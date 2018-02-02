# -*- coding:utf-8 -*-
import os
import threading
import time

from boto3 import Session

# session = boto3.session.Session()

BUCKET_NAME = 'XXcloud_sandbox'  # replace with your bucket name
KEY = 'schema.json'  # replace with your object key
sample_file = './__init__.py'
sample_file_key = 'aaa/2018/02/03/s3_sample_1'

ak = 'VmpGb2QxTXdNVVpPVm1ScVVtMTRjRlZxVG05WGJGSllZM3BHYkdKSGVIaFdSM2hyWVVVeFdGcEVXbGRTZWtaMldWWmtTMVl4VG5WUmJIQm9ZWHBXTVZWNlRtcGphM1F6UzNsekt3Kys+'
sk = '791867e3bc334355aa28d97e2985ee08'
manager_ep = 'http://10.95.166.211:50841'
resource_ep = 'http://10.95.166.211:50840'

# s3 = boto3.resource(service_name='s3',
#                     aws_access_key_id=ak,
#                     aws_secret_access_key=sk,
#                     endpoint_url=resource_ep)
#
# client = boto3.client(service_name='s3',
#                       aws_access_key_id=ak,
#                       aws_secret_access_key=sk,
#                       endpoint_url=resource_ep)

"""
官方方法列表参见：http://boto3.readthedocs.io/en/latest/reference/services/s3.html?highlight=endpoint#S3.Client
"""


class ResourceManager():
    def __init__(self, aws_access_key_id, aws_secret_access_key, endpoint_url):
        self.session = Session(aws_access_key_id, aws_secret_access_key)
        self.url = endpoint_url  # 例如：'http://IP:PORT' 或者 'http://eos-beijing1.cmecloud.cn'或者'http://eos-beijing-2.cmecloud.cn'
        self.s3_client = self.session.client('s3', endpoint_url=self.url)

    def upload(self, key, file_path):
        resp = self.s3_client.put_object(Bucket=BUCKET_NAME, Key=key, Body=open(file_path, 'rb').read())
        print resp

    """
    分片上传
    1. 初始化（createMultipartUpload）：获得Upload ID
    2. 上传分片（uploadPart）：这一步可以并发进行
    3. 完成上传（completeMultipartUpload）：合并分片，生成文件
    """


    def upload_by_multipart(self, file_key, file_name):
        s= time.time()
        mpu = self.s3_client.create_multipart_upload(Bucket=BUCKET_NAME, Key=file_key)  # step1.初始化
        part_info = {
            'Parts': []
        }
        i = 1
        f = open(file_name, 'rb')
        while 1:
            data = f.read(10 * 1024 * 1024)  # 每个分块10MiB大小，可调整
            if not data:
                break
            response = self.s3_client.upload_part(Bucket=BUCKET_NAME, Key=file_key, PartNumber=i,
                                                   UploadId=mpu["UploadId"], Body=data)  # step2.上传分片 #可改用多线程
            part_info['Parts'].append({'PartNumber': i, 'ETag': response['ETag']
                                        })
            i += 1
        self.s3_client.complete_multipart_upload(Bucket=BUCKET_NAME, Key=file_key, UploadId=mpu["UploadId"],
                                                 MultipartUpload=part_info)  # step3.完成上传
        print 'upload successful',time.time()-s

    """
    多线程版本的分片上传
    """
    def upload_by_multipart_by_thread(self, file_key, file_name):
        s=time.time()
        mpu = self.s3_client.create_multipart_upload(Bucket=BUCKET_NAME, Key=file_key)  # step1.初始化
        part_info = {
            'Parts': []
        }
        i = 1
        f = open(file_name, 'rb')
        while 1:
            data = f.read(10 * 1024 * 1024)  # 每个分块10MiB大小，可调整
            if not data:
                break
            thread = threading.Thread(target=self.upload_part,args=(data, file_key, i, mpu, part_info))
            thread.start()
            i += 1
        while True:
            print len(part_info['Parts']),i
            if len(part_info['Parts'])== (i-1):
                print part_info
                time.sleep(1)
                self.s3_client.complete_multipart_upload(Bucket=BUCKET_NAME, Key=file_key, UploadId=mpu["UploadId"],
                                                 MultipartUpload=part_info)  # step3.完成上传
                print 'upload successful',time.time()-s
                break
            else:
                time.sleep(1)
                print 'uploading'

    def upload_part(self, data, file_key, i, mpu, part_info):
        print 'start to upload part: %s ' % i
        response = self.s3_client.upload_part(Bucket=BUCKET_NAME, Key=file_key, PartNumber=i,
                                              UploadId=mpu["UploadId"], Body=data)  # step2.上传分片 #可改用多线程
        part_info['Parts'].append({'PartNumber': i, 'ETag': response['ETag']})
        print 'part %s upload successful!'% i,response['ETag']

    def head(self, key):
        resp = self.s3_client.head_object(Bucket=BUCKET_NAME, Key=key)
        print resp['Body']

    def upload_str_obj(self, str_obj):
        put_resp = self.s3_client.put_object(Bucket=BUCKET_NAME, Key='key', Body=str_obj)
        get_resp = self.s3_client.get_object(Bucket=BUCKET_NAME, Key='key')
        print 'put resp:%s' % put_resp
        print 'put resp type:%s' % type(get_resp['Body'])
        print 'put resp:%s' % get_resp['Body'].read()

    def download(self,key):
        resp = self.s3_client.get_object(Bucket=BUCKET_NAME, Key=key)
        # resp = client.get_object(Bucket=BUCKET_NAME, Key=sample_file)
        with open('./download', 'wb') as f:
            f.write(resp['Body'].read())

    #
    def list_files(self):
        resp = self.s3_client.list_objects(Bucket=BUCKET_NAME)
        for obj in resp['Contents']:
            print obj['Key']
        # 目前API没有实现
        # raise NotImplementedError('Backend API Not implemented!')

    def delete(self):
        resp = self.s3_client.delete_object(Bucket=BUCKET_NAME, Key='schema.json')
        print resp

    def exist(self, key):
        # try:
        #     self.s3_client.head_object(Bucket=BUCKET_NAME, Key=key)
        #     print "EXIST"
        # except BaseException,ex:
        #     print ex
        #     print "NOT FOUND"
        raise NotImplementedError('Backend API Not implemented!')


class AdminManager():
    def __init__(self, aws_access_key_id, aws_secret_access_key, endpoint_url):
        self.access_key = aws_access_key_id
        self.secret_key = aws_secret_access_key
        self.session = Session(self.access_key, self.secret_key)
        self.url = endpoint_url  # 例如：'http://IP:PORT' 或者 'http://eos-beijing1.cmecloud.cn'或者'http://eos-beijing-2.cmecloud.cn'
        self.s3_client = self.session.client('s3', endpoint_url=self.url)

    def create_bucket(self, name):
        self.s3_client.create_bucket(Bucket=name, ACL='public-read')

    def get_bucket_location(self, name):
        # self.s3_client.get_bucket_location(Bucket=name)
        raise NotImplementedError('Backend API Not implemented!')

    def get_bucket_acl(self, name):
        print self.s3_client.get_bucket_acl(Bucket=name)['Owner']
        # raise NotImplementedError('Backend API Not implemented!')

    def get_buckets(self):
        print [bucket for bucket in self.s3_client.list_buckets()]

    def get_bucket_info(self):
        resp = self.s3_client.head_bucket(Bucket=BUCKET_NAME)
        print "使用空间（字节）：", resp['ResponseMetadata']['HTTPHeaders']['xrgw-bytes-used']
        print "桶内对象个数:", resp['ResponseMetadata']['HTTPHeaders']['x-rgwobject-count']


if __name__ == '__main__':
    # resource = AdminManager(ak, sk, manager_ep)
    # resource.get_bucket_acl('test_bucket')
    # resource.get_buckets()
    # resource.get_bucket_info()
    # resource.create_bucket('XXcloud_sandbox')

    resource = ResourceManager(ak, sk, resource_ep)
    # resource.list_files();
    # resource.upload_str_obj('asdlkfasldkfalsdkfalsdkfalsdkfalsdkfj')
    resource.upload(sample_file_key,sample_file)
    # resource.download()
    # resource.download('kibana.zip')
    # resource.head(sample_file)
    # resource.exist(sample_file)
    #resource.upload_by_multipart('kibana.zip', './500Mfile')
    #resource.upload_by_multipart_by_thread('kibana.zip', './500Mfile')
