# -*- coding:utf-8 -*-
import hashlib
import json
import threading
import time
import traceback

import faker
from datetime import datetime

from etl import utils
from etl.extractors import write_result_to_es, write_result_to_es_by_bulk
from random_s.fake_provider import *

DATA_SIZE = 200000000
BATCH_SIZE = 1000

class FakeDataFactory():
    @staticmethod
    def gen_url_date(counts=DATA_SIZE):
        fake = faker.Faker()
        fake.add_provider(EnvProvider)
        fake.add_provider(DomainProvider)
        fake.add_provider(IPProvider)
        fake.add_provider(URLProvider)
        fake.add_provider(SignatureProvider)
        index = 0
        map_list = []
        while index < counts:
            random_drop_content = fake.text()
            random_url = fake.url()
            start_time = time.time()
            result_map = {'check_envrionment': {'os_evn': fake.env(), 'analyzer': 'cuckoo'},
                          'check_status': {'code': random.randint(1, 10), 'msg': fake.text()},
                          'droped_file': [{'md5': hashlib.md5(random_drop_content).hexdigest(),
                                           'name': random_drop_content,
                                           'sha1': hashlib.sha1(random_drop_content).hexdigest(),
                                           'sha256': hashlib.sha256(random_drop_content).hexdigest(),
                                           'sha512': hashlib.sha512(random_drop_content).hexdigest(),
                                           'type': fake.text()},
                                          ],
                          'end_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                          'network_domain': [fake.domain() for i in range(random.randint(1, 50))],
                          'network_ip': [fake.ip() for i in range(random.randint(1, 50))],
                          'network_url': [fake.url() for i in range(random.randint(1, 10))],
                          'result_path': 'D:/sc/git/python_cookbook/etl/%s' % hashlib.sha1(
                              random_drop_content).hexdigest(),
                          'signature_rule': fake.signature(),
                          'start_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                          'url': random_url,
                          'url_md5': hashlib.md5(random_url).hexdigest(),
                          'url_score': 1.2,
                          'url_sha1': hashlib.sha1(random_url).hexdigest()}
            # print result_map
            map_list.append(json.dumps(result_map))
            if index % BATCH_SIZE == 0:
                write_result_to_es_by_bulk(map_list, utils.url_check_result_index_name)
                print 'generate batch file fake date use:%s' % str(time.time() - start_time)
                map_list = []
            index = index + 1

    @staticmethod
    def gen_file_date(counts=DATA_SIZE):
        fake = faker.Faker()
        fake.add_provider(EnvProvider)
        fake.add_provider(DomainProvider)
        fake.add_provider(IPProvider)
        fake.add_provider(URLProvider)
        fake.add_provider(SignatureProvider)
        index = 0
        map_list = []
        while index < counts:
            random_drop_content = fake.text()
            random_file_name = fake.url()
            start_time = time.time()
            result_map = {'check_envrionment': {'os_evn': fake.env(), 'analyzer': 'cuckoo'},
                          'check_status': {'code': random.randint(1, 10), 'msg': fake.text()},
                          'droped_file': [{'md5': hashlib.md5(random_drop_content).hexdigest(),
                                           'name': random_drop_content,
                                           'sha1': hashlib.sha1(random_drop_content).hexdigest(),
                                           'sha256': hashlib.sha256(random_drop_content).hexdigest(),
                                           'sha512': hashlib.sha512(random_drop_content).hexdigest(),
                                           'type': fake.text()},
                                          ],
                          'end_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                          'network_domain': [fake.domain() for i in range(random.randint(1, 50))],
                          'network_ip': [fake.ip() for i in range(random.randint(1, 50))],
                          'network_url': [fake.url() for i in range(random.randint(1, 10))],
                          'result_path': 'D:/sc/git/python_cookbook/etl/%s' % hashlib.sha1(
                              random_drop_content).hexdigest(),
                          'signature_rule': fake.signature(),
                          'start_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                          'file_name': random_file_name,
                          'file_md5': hashlib.md5(random_file_name).hexdigest(),
                          'file_sha1': hashlib.sha1(random_drop_content).hexdigest(),
                          'file_sha256': hashlib.sha256(random_drop_content).hexdigest(),
                          'file_sha512': hashlib.sha512(random_drop_content).hexdigest(),
                          'file_type': fake.text(),
                          'is_virus': random.choice([True, False]),
                          'virus_name': fake.text()[1:20],
                          'thread_level': random.randint(1, 100),
                          'malware_score': random.randint(1, 100),
                          'file_score': random.randint(1, 100),
                          }
            # print result_map
            map_list.append(json.dumps(result_map))
            if index % BATCH_SIZE == 0:
                write_result_to_es_by_bulk(map_list, utils.file_check_result_index_name)
                print 'generate batch file fake date use:%s' % str(time.time() - start_time)
                map_list=[]
            index = index + 1


if __name__ == '__main__':
    # fire.Fire(FakeDataFactory)
    try:
        # FakeDataFactory().gen_url_date()
        # FakeDataFactory().gen_file_date()
        f_thread = threading.Thread(target=FakeDataFactory.gen_file_date)
        url_thread = threading.Thread(target=FakeDataFactory.gen_url_date)
        f_thread.start()
        url_thread.start()
    except:
        traceback.print_exc()
