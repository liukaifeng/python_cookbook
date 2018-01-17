# -*- coding:utf-8 -*-
import unittest
import datetime
from datetime import timedelta
import time
from pprint import pprint

from elasticsearch import Elasticsearch


class URLCheckresultTestCase(unittest.TestCase):
    def setUp(self):
        self.es_client = Elasticsearch(hosts=['127.0.0.1'],
                                       sniff_on_start=True,
                                       sniff_on_connection_fail=True,
                                       sniffer_timeout=60
                                       )
        self.index = 'skyeye_cloud_sandbox_url'
        self.type = 'result'

    def tearDown(self):
        pass

    def test_find_url_result_from_file_path(self):
        res = self.es_client.search(index=self.index, doc_type=self.type,
                                    body={"query": {"term": {"result_path": "2901_ab877511ce28325f31f1e398827834fa"}}})
        print("Got %d Hits:" % res['hits']['total'])

    def test_find_url_result_from_term(self):
        res = self.es_client.search(index=self.index, doc_type=self.type,
                                    body={"query": {"term": {"url_sha1": "d87edbd0e0c73fe36b9be6c9cbb1c368cc0c49ec"}}})
        print("Got %d Hits:" % res['hits']['total'])

    def test_find_url_result_from_wildcard(self):
        res = self.es_client.search(index=self.index, doc_type=self.type,
                                    body={"query": {"wildcard": {"url_sha1": "*b9be6c9cbb1c368cc0c4*"}}})
        print("Got %d Hits:" % res['hits']['total'])

    def test_find_url_result_from_filter(self):
        now = datetime.datetime.now()
        yesterday = now - timedelta(hours=1)

        res = self.es_client.search(index=self.index, doc_type=self.type,
                                    body={"query": {"bool": {
                                        "must": [
                                            {"match": {"url": "http://www.so.com"}}
                                        ],
                                        "filter": [
                                            {
                                                "term": {
                                                    "signature_rule": "network_http"
                                                }

                                            },
                                            {
                                                "range":
                                                    {"start_time":
                                                        {
                                                            "gte": yesterday.strftime("%Y-%m-%d %H:%M:%S")
                                                        }
                                                    }
                                            }
                                        ]
                                    }}})
        print("Got %d Hits:" % res['hits']['total'])

    def test_find_url_result_from_list(self):
        res = self.es_client.search(index=self.index, doc_type=self.type,
                                    body={"query": {"term": {"network_ip": "172.16.1.101"}}})
        print("Got %d Hits:" % res['hits']['total'])

    def test_find_url_result_nested(self):
        res = self.es_client.search(index=self.index, doc_type=self.type, body={
            "query": {"term": {"droped_file.sha1": "fe815ae0f865ec4c26e421bf0bd21bb09bc6f410"}}})
        pprint(res)
        print("Got %d Hits:" % res['hits']['total'])

    def test_find_result_by_time_range(self):
        res = self.es_client.search(index=self.index, doc_type=self.type, body={
            "query": {"term": {"droped_file.sha1": "fe815ae0f865ec4c26e421bf0bd21bb09bc6f410"}}})
        pprint(res)
        print("Got %d Hits:" % res['hits']['total'])
