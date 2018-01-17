# -*- coding:utf-8 -*-
from elasticsearch import Elasticsearch, Urllib3HttpConnection

file_field_type_mapping = {
    'static': ['file_name', 'file_md5', 'file_path', 'file_sha1', 'file_sha256', 'file_sha512', 'file_type', 'is_virus',
               'threat_level', 'malware_score'],
}

file_check_result_index_name = 'skyeye_cloud_sandbox_file'
url_check_result_index_name = 'skyeye_cloud_sandbox_url'

es_client = Elasticsearch(hosts=['127.0.0.1'],
                          # sniff_on_start=True,
                          retry_on_timeout = True,
                          sniff_on_connection_fail=True,
                          request_timeout=5,
                          # connection_class= Urllib3HttpConnection,
                          sniffer_timeout=60
                          )
