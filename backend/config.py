import boto3
from botocore.client import Config

class boto3_conf:
    S3_BUCKET_NAME = 'bucket-de6ad0'
    session = boto3.session.Session(profile_name='default')
    s3_client = session.client(
   service_name='s3',
   endpoint_url='https://s3.cloud.ru'
)