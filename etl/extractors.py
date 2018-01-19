# -*- coding:utf-8 -*-
import os
import json
import time
import logging
import hashlib
import traceback
from elasticsearch import helpers, Elasticsearch, Urllib3HttpConnection

log = logging.getLogger(__name__)
FILE_FIELD_TYPE_MAPPING = {
    'static': ['file_name', 'file_md5', 'file_path', 'file_sha1', 'file_sha256',
               'file_sha512', 'file_type', 'is_virus', 'threat_level', 'malware_score'],
}
FILE_CHECK_RESULT_INDEX_NAME = 'skyeye_cloud_sandbox_file'
URL_CHECK_RESULT_INDEX_NAME = 'skyeye_cloud_sandbox_url'


def is_exists(file_dir):
    return os.path.exists(file_dir)


def open_file(file_path):
    if is_exists(file_path):
        with open(file_path, 'rb') as data_file:
            data = json.load(data_file)
            return data
    return None


# 用于读取一个文件包含多行Json的情况
def open_multi_json_line_file(file_path):
    if is_exists(file_path):
        json_list = []
        with open(file_path, 'rb') as data_file:
            lines = data_file.readlines()
            for line in lines:
                data = json.loads(line)
                json_list.append(data)
            return json_list
    return None


class EsUtils(object):
    ES_HOSTS = ['1.192.194.26']

    def __init__(self, es_hosts=None):
        self.es_hosts = es_hosts if es_hosts else self.ES_HOSTS
        self.es_client = Elasticsearch(hosts=self.es_hosts,
                                       connection_class=Urllib3HttpConnection,
                                       sniffer_timeout=60)

    def proccess_static_file(self, file_dir, result_map):
        static_result = open_file('%s%sstatic.json' % (file_dir, os.path.sep,))
        if static_result:
            for field in FILE_FIELD_TYPE_MAPPING['static']:
                result_map[field] = static_result['base_info'].get(field, '')
            # 需要特殊处理'virus_name'
            for detail_info in static_result['detail_info'].values():
                if detail_info.get('virus_name', ''):
                    result_map['virus_name'] = detail_info['virus_name']
        else:
            raise Exception("File not exists")

    def _get_sub_tag_values(self, dynamic_result, first_tag, second_tag):
        result_list = []
        for protocol_actions in dynamic_result[first_tag].values():
            for protocol_action in protocol_actions:
                if isinstance(protocol_action, dict) and protocol_action.get(second_tag, ''):
                    result_list.append(protocol_action[second_tag])
        return list(set(result_list))

    def _extract_common_info(self, dynamic_result, result_map):
        # signature_rule：signatures/name
        result_map['signature_rule'] = [signature['name'] for signature in dynamic_result['signatures']]
        # network_ip:network/*/dip
        result_map['network_ip'] = self._get_sub_tag_values(dynamic_result, 'network', 'dst')
        result_map['network_domain'] = [domain['domain'] for domain in dynamic_result['network']['domains']]
        # droped_file:dropped
        result_map['droped_file'] = [{'name': droped_file['name'], 'type': droped_file['type'],
                                      'md5': droped_file['md5'], 'sha1': droped_file['sha1'],
                                      'sha256': droped_file['sha256'], 'sha512': droped_file['sha512']}
                                     for droped_file in dynamic_result.get('dropped', [])]
        # start_time:info/start_time
        # result_map['start_time'] = dynamic_result['info'].get('start_time', '')
        # end_time:info/end_time
        # result_map['end_time'] = dynamic_result['info'].get('end_time', '')

    def proccess_file_runtime_file(self, file_dir, result_map):
        dynamic_result = open_file('%s%sreports/report.json' % (file_dir, os.path.sep,))
        if dynamic_result:
            # file_score:info/score
            result_map['file_score'] = dynamic_result['info']['score']
            # signature_info:static/signature
            result_map['signature_info'] = dynamic_result.get('static', {}).get('signature', [])
            # network_url:target/urls
            result_map['network_url'] = dynamic_result.get('target', {}).get('file', {}).get('urls', [])
            self._extract_common_info(dynamic_result, result_map)

    def proccess_task_file(self, file_dir, result_map):
        task_info = open_file('%s%s/task.json' % (file_dir, os.path.sep,))
        if task_info:
            print task_info['submit_info']
            result_map['task_id'] = task_info['submit_info']['task_id']
            result_map['start_time'] = task_info['submit_info']['accept_time']
            result_map['end_time'] = task_info['submit_info']['finish_time']
            result_map['sample_path'] = task_info['submit_info'].get('remote_path', '')
            result_map['result_path'] = task_info['submit_info']['result_path']
            result_map['check_status'] = task_info['submit_info'].get('check_status', {})
            result_map['check_envrionment'] = {'machine': task_info['submit_info']['check_param'].get('machine',''),
                                               'analyzer': task_info['submit_info'].get('analyze_type','')}
        else:
            raise Exception("File not exists")

    def proccess_shot_file(self, file_dir, result_map):
        jsons = open_multi_json_line_file('%s%s/files.json' % (file_dir, os.path.sep,))
        if jsons:
            screen_list = []
            for json_line in jsons:
                if json_line.get('path', '').startswith('shots'):
                    screen_list.append(json_line['path'])
            result_map['screen'] = list(set(screen_list))

    def proccess_url_runtime_file(self, file_dir, result_map):
        dynamic_result = open_file('%s%sreports/report.json' % (file_dir, os.path.sep,))
        if dynamic_result:
            target_url = dynamic_result.get('target', {}).get('url', '')
            result_map['url'] = target_url
            result_map['url_md5'] = hashlib.md5(target_url).hexdigest()
            result_map['url_sha1'] = hashlib.sha1(target_url).hexdigest()
            result_map['url_score'] = dynamic_result['info']['score']
            url_list = []
            for dropped_action in dynamic_result['dropped']:
                for dropped_url in dropped_action.get('urls', []):
                    url_list.append(dropped_url)
            result_map['network_url'] = list(set(url_list))
            self._extract_common_info(dynamic_result, result_map)
        else:
            raise Exception("File not exists")

    def write_result_to_es(self, result_map, index, doc_type='result'):
        response = self.es_client.index(index=index, doc_type=doc_type, body=result_map)
        if not response.get('created', ''):
            raise Exception('write es failed')

    def write_result_to_es_by_bulk(self, result_maps, index, doc_type='result'):
        try:
            actions = [
                {
                    '_op_type': 'index',
                    '_index': index,
                    '_type': doc_type,
                    '_source': d
                }
                for d in result_maps
            ]
            response = helpers.bulk(client=self.es_client, actions=actions)
            log.info('Response: %s', response)
        except BaseException, ex:
            log.error('Error: %s', ex)
            traceback.print_exc()

    def extractor_file_check_result(self, file_dir):
        if is_exists(file_dir):
            try:
                result_map = {}
                s_time = time.time()
                self.proccess_static_file(file_dir, result_map)
                self.proccess_file_runtime_file(file_dir, result_map)
                self.proccess_task_file(file_dir, result_map)
                self.proccess_shot_file(file_dir, result_map)
                self.write_result_to_es(result_map, FILE_CHECK_RESULT_INDEX_NAME)
                log.info('Process %s dir elapsed:%s ', file_dir, str(time.time() - s_time))
                return True
            except Exception, ex:
                log.error('Error: %s', ex)
                traceback.print_exc()
                return False
        return False

    def extractor_url_check_result(self, file_dir):
        if is_exists(file_dir):
            try:
                result_map = {}
                s_time = time.time()
                self.proccess_url_runtime_file(file_dir, result_map)
                self.proccess_task_file(file_dir, result_map)
                self.proccess_shot_file(file_dir, result_map)
                self.write_result_to_es(result_map, URL_CHECK_RESULT_INDEX_NAME)
                log.info('Process %s dir elapsed:%s ', file_dir, str(time.time() - s_time))
                return True
            except Exception, ex:
                log.error('Error: %s', ex)
                traceback.print_exc()
                return False
        return False


if __name__ == '__main__':
    es = EsUtils()
    es.extractor_file_check_result("D:/sc/git/python_cookbook/etl/000000000106d770cea0f634f14df3fb9b99ddf4")
    # es.extractor_url_check_result("D:/sc/git/python_cookbook/etl/0336_ab877511ce28325f31f1e398827834fa")
    # es.extractor_url_check_result("D:/sc/git/python_cookbook/etl/2901_ab877511ce28325f31f1e398827834fa")
    # es.extractor_url_check_result("D:/sc/git/python_cookbook/etl/445302318a754322c5d3209f8d444f5bf0b051ee")
