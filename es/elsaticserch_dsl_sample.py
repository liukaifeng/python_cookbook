# -*- coding:utf-8 -*-
import random
import hashlib

from elasticsearch_dsl import DocType, Keyword
from elasticsearch_dsl.connections import connections

index_prefix = 'skyeye_cloud_sandbox_s3_index_%s'
connections.create_connection(hosts=['10.95.166.208', '10.95.166.209', '10.95.166.210'])

class Doc(DocType):
    task_id = Keyword()
    file_name = Keyword()

    class Meta:
        index = 'skyeye_cloud_sandbox_s3_index_*'

    def save(self, **kwargs):
        # 使用索引模板生成索引
        index = index_prefix % (self.task_id[0])
        return super(Doc, self).save(index=index, **kwargs)

if __name__ == '__main__':
    for i in range(100):
        s3index = Doc(task_id = str(hashlib.md5(str(random.randint(0,100))).hexdigest()),file_name = str(hashlib.md5(str(random.randint(0,100))).hexdigest()))
        s3index.save()
        print 'finish done!'