import boto3
from botocore.client import Config
from flask import Flask


class app_conf:
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://myuser:mypassword@localhost:5432/smm'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['SECRET_KEY'] = 'your-secret-key'  # Секретный ключ для подписи сессий


class boto3_conf:
    S3_BUCKET_NAME = 'bucket-de6ad0'
    session = boto3.session.Session(profile_name='default')
    s3_client = session.client(
   service_name='s3',
   endpoint_url='https://s3.cloud.ru'
)