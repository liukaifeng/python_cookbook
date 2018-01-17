# -*- coding:utf-8 -*-

import string
from faker.providers import BaseProvider
from faker.generator import random

"""
定义Fake的Provider用来生成假数据
"""

class EnvProvider(BaseProvider):
    def env(self):
        os_evn_list = 'flash17.0.0.188,cn,sp1,windows7,agent,java7,office2010,ie11,adobe_reader9.0.0,x86'.split(',')
        return ','.join(random.sample(os_evn_list, 2))


class IPProvider(BaseProvider):
    def ip(self):
        return '.'.join(
            [str(random.randint(1, 255)) for i in range(4)])


class URLProvider(BaseProvider):
    def url(self):
        return 'http://%s ' % '.'.join(
            [''.join(random.sample(string.ascii_lowercase, random.randint(4, 10))) for i in
             range(random.randint(3, 6))])


class DomainProvider(BaseProvider):
    def domain(self):
        return '.'.join(
            [''.join(random.sample(string.ascii_lowercase, random.randint(4, 10))) for i in
             range(random.randint(3, 6))])


class SignatureProvider(BaseProvider):
    def signature(self):
        os_evn_list = [u'network_http', u'allocates_rwx', u'creates_exe']
        return random.sample(os_evn_list, 2)
