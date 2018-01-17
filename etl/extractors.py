# -*- coding:utf-8 -*-
import hashlib
import json
import os
import time
import traceback
from pprint import pprint

import elasticsearch.helpers

import utils


# TODO:需要根据文件提供的方式重写该接口
def dir_exists(file_dir):
    return True


# TODO:需要根据文件提供的方式重写该接口
def open_file(file_path):
    if os.path.exists(file_path):
        # print file_path
        with open(file_path, 'r') as data_file:
            data = json.load(data_file)
            return data
    return None


def proccess_static_file(file_dir, result_map):
    static_result = open_file('%s%sstatic.json' % (file_dir, os.path.sep,))
    if static_result:
        for field in utils.file_field_type_mapping['static']:
            result_map[field] = static_result['base_info'].get(field, '')
        # 需要特殊处理'virus_name'
        for detail_info in static_result['detail_info'].values():
            if detail_info.get('virus_name', ''):
                result_map['virus_name'] = detail_info['virus_name']
    else:
        raise Exception("File not exists")


def _get_sub_tag_values(dynamic_result, first_tag, second_tag):
    result_list = []
    for protocol_actions in dynamic_result[first_tag].values():
        for protocol_action in protocol_actions:
            if isinstance(protocol_action, dict) and protocol_action.get(second_tag, ''):
                result_list.append(protocol_action[second_tag])
    return list(set(result_list))


def _extract_common_info(dynamic_result, result_map):
    # signature_rule：signatures/name
    result_map['signature_rule'] = [signature['name'] for signature in dynamic_result['signatures']]
    # network_ip:network/*/dip
    result_map['network_ip'] = _get_sub_tag_values(dynamic_result, 'network', 'dst')
    # pprint( dynamic_result.get('target', {}).get('file', {}))
    # network_domain:network/domains/domain
    result_map['network_domain'] = [domain['domain'] for domain in dynamic_result['network']['domains']]
    # droped_file:dropped
    result_map['droped_file'] = [{'name': droped_file['name'], 'type': droped_file['type'], 'md5': droped_file['md5'],
                                  'sha1': droped_file['sha1'], 'sha256': droped_file['sha256'],
                                  'sha512': droped_file['sha512'], } for droped_file in
                                 dynamic_result.get('dropped', [])]
    # start_time:info/start_time
    result_map['start_time'] = dynamic_result['info'].get('start_time', '')
    # end_time:info/end_time
    result_map['end_time'] = dynamic_result['info'].get('end_time', '')
    # check_envrionment:info/check_envrionment
    result_map['check_envrionment'] = dynamic_result['info'].get('check_envrionment', {})
    # check_status:info/check_envrionment
    result_map['check_status'] = dynamic_result['info'].get('check_status', {})


def proccess_file_runtime_file(file_dir, result_map):
    dynamic_result = open_file('%s%sreports/report.json' % (file_dir, os.path.sep,))
    # print dynamic_result
    if dynamic_result:
        # file_score:info/score
        result_map['file_score'] = dynamic_result['info']['score']
        # signature_info:static/signature
        result_map['signature_info'] = dynamic_result.get('static', {}).get('signature', [])
        # network_url:target/urls
        result_map['network_url'] = dynamic_result.get('target', {}).get('file', {}).get('urls', [])
        _extract_common_info(dynamic_result, result_map)
    else:
        raise Exception("File not exists")


def proccess_url_runtime_file(file_dir, result_map):
    dynamic_result = open_file('%s%sreports/report.json' % (file_dir, os.path.sep,))
    # print dynamic_result
    if dynamic_result:
        target_url = dynamic_result.get('target', {}).get('url', '')
        result_map['url'] = target_url
        result_map['url_md5'] = hashlib.md5(target_url).hexdigest()
        result_map['url_sha1'] = hashlib.sha1(target_url).hexdigest()
        result_map['url_score'] = dynamic_result['info']['score']
        # network_url:target/urls
        url_list = []
        for dropped_action in dynamic_result['dropped']:
            for dropped_url in dropped_action.get('urls', []):
                url_list.append(dropped_url)
        result_map['network_url'] = list(set(url_list))
        _extract_common_info(dynamic_result, result_map)
    else:
        raise Exception("File not exists")


def write_result_to_es(result_map, index, doc_type='result'):
    try:
        response = utils.es_client.index(index=index, doc_type=doc_type, body=result_map)
        if response.get('created', '') != True:
            traceback.print_exc()
            # raise Exception('write es failed')
    except BaseException, ex:
        print ex
        traceback.print_exc()


def write_result_to_es_by_bulk(result_maps, index, doc_type='result'):
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
        response = elasticsearch.helpers.bulk(client=utils.es_client, actions=actions)
        print response
    except BaseException, ex:
        print ex
        traceback.print_exc()


def extractor_file_check_result(file_dir):
    if dir_exists(file_dir):
        try:
            result_map = {}
            s_time = time.time()
            proccess_static_file(file_dir, result_map)
            proccess_file_runtime_file(file_dir, result_map)
            # 处理result_path
            result_map['result_path'] = file_dir
            pprint(result_map)
            write_result_to_es(result_map, utils.file_check_result_index_name)
            print 'Process %s dir elapsed:%s ' % (file_dir, str(time.time() - s_time))
            return True
        except Exception, ex:
            print '####:', ex
            traceback.print_exc()
            return False
    return False


def extractor_url_check_result(file_dir):
    if dir_exists(file_dir):
        try:
            result_map = {}
            s_time = time.time()
            proccess_url_runtime_file(file_dir, result_map)
            # 处理result_path
            result_map['result_path'] = file_dir
            write_result_to_es(result_map, utils.url_check_result_index_name)
            print 'Process %s dir elapsed:%s ' % (file_dir, str(time.time() - s_time))
            pprint(result_map)
            return True
        except Exception, ex:
            print '####:', ex
            traceback.print_exc()
            return False
    return False


if __name__ == '__main__':
    # extractor_file_check_result("D:/sc/git/python_cookbook/etl/4458_ce52d039f3229e6ba37247bbe0eee31e")
    # extractor_url_check_result("D:/sc/git/python_cookbook/etl/0336_ab877511ce28325f31f1e398827834fa")
    extractor_url_check_result("D:/sc/git/python_cookbook/etl/2901_ab877511ce28325f31f1e398827834fa")
