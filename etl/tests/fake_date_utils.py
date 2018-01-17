# -*- coding:utf-8 -*-
import hashlib
import time

import faker
from datetime import datetime

from etl import utils
from etl.extractors import write_result_to_es
from random_s.fake_provider import *


class FakeDataFactory():
    def gen_url_date(self, counts=1000):
        fake = faker.Faker()
        fake.add_provider(EnvProvider)
        fake.add_provider(DomainProvider)
        fake.add_provider(IPProvider)
        fake.add_provider(URLProvider)
        fake.add_provider(SignatureProvider)
        index = 0
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
                          'result_path': 'D:/sc/git/python_cookbook/etl/%s' % hashlib.sha1(random_drop_content).hexdigest(),
                          'signature_rule': fake.signature(),
                          'start_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                          'url': random_url,
                          'url_md5': hashlib.md5(random_url).hexdigest(),
                          'url_score': 1.2,
                          'url_sha1': hashlib.sha1(random_url).hexdigest()}
            # print result_map
            print 'generate fake date use:%s' % str(time.time() - start_time)
            write_result_to_es(result_map, utils.url_check_result_index_name)
            index = index + 1

    def gen_file_date(self, counts=1000):
        fake = faker.Faker()
        fake.add_provider(EnvProvider)
        fake.add_provider(DomainProvider)
        fake.add_provider(IPProvider)
        fake.add_provider(URLProvider)
        fake.add_provider(SignatureProvider)
        index = 0
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
                          'result_path': 'D:/sc/git/python_cookbook/etl/%s' % hashlib.sha1(random_drop_content).hexdigest(),
                          'signature_rule': fake.signature(),
                          'start_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                          'file_name': random_file_name,
                          'file_md5': hashlib.md5(random_file_name).hexdigest(),
                          'file_sha1': hashlib.sha1(random_drop_content).hexdigest(),
                          'file_sha256': hashlib.sha256(random_drop_content).hexdigest(),
                          'file_sha512': hashlib.sha512(random_drop_content).hexdigest(),
                          'file_type': fake.text(),
                          'is_virus': random.choice([True,False]),
                          'virus_name': fake.text()[1:20],
                          'thread_level':random.randint(1,100),
                          'malware_score':random.randint(1,100),
                          'file_score':random.randint(1,100),
                          }
            # print result_map
            print 'generate fake date use:%s' % str(time.time() - start_time)
            write_result_to_es(result_map, utils.file_check_result_index_name)
            index = index + 1


if __name__ == '__main__':
    # fire.Fire(FakeDataFactory)
    FakeDataFactory().gen_url_date()
    FakeDataFactory().gen_file_date()

