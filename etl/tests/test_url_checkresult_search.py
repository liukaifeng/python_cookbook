# -*- coding:utf-8 -*-
import unittest

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

    def test_find_url_result_by_http_url(self):
        res=self.es_client.search(index=self.index, body={"query": {"term": {"url": "http://www.so.com"}}})
        print("Got %d Hits:" % res['hits']['total'])

    def test_find_url_result_by_url(self):
        res=self.es_client.search(index=self.index, body={"query": {"term": {"url": "www.so.com"}}})
        print("Got %d Hits:" % res['hits']['total'])

    def test_find_url_result_by_network_url(self):
        res=self.es_client.search(index=self.index, body={"query": {"term": {"network_ip": "172.16.1.101"}}})
        print("Got %d Hits:" % res['hits']['total'])

    def test_find_url_result_by_dopped_file_props(self):
        res=self.es_client.search(index=self.index, body={"query": {"term": {"droped_file.sha1": "fe815ae0f865ec4c26e421bf0bd21bb09bc6f410"}}})
        print("Got %d Hits:" % res['hits']['total'])
