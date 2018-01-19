# -*- coding:utf-8 -*-
import unittest
import datetime
from datetime import timedelta
import time
from pprint import pprint

from elasticsearch import Elasticsearch


class URLCheckresultTestCase(unittest.TestCase):
    def setUp(self):
        self.es_client = Elasticsearch(hosts=['1.192.194.26'],
                                       sniff_on_start=True,
                                       sniff_on_connection_fail=True,
                                       sniffer_timeout=60
                                       )
        self.index = 'skyeye_cloud_sandbox_file'
        self.type = 'result'

    def tearDown(self):
        pass



    def test_find_file_result_from_term(self):
        res = self.es_client.search(index=self.index, doc_type=self.type,
                                    body={"query": {"term": {"task_id": "111111110106d770cea0f634f14df3fb9b99ddf4"}}})
        pprint (res)
        print("Got %d Hits:" % res['hits']['total'])




