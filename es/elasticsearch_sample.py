# -*- coding:utf-8 -*-
from elasticsearch import Elasticsearch

es_client = Elasticsearch(hosts=['10.95.166.208', '10.95.166.209', '10.95.166.210'],
                          sniffer_timeout=60)


def persist():
    body = {
        'file_name': 'abc',
        'task_id': '123'
    }
    res = es_client.index(index='skyeye_cloud_sandbox_s3_index_1', doc_type='s3_file_index', body=body)
    print res


if __name__ == '__main__':
    persist()
