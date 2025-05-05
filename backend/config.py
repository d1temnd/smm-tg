import boto3
import os
from pika import ConnectionParameters
from botocore.client import Config
from flask import Flask
from flask_caching import Cache
import redis
from flask_cors import CORS
import logging
from logging.handlers import RotatingFileHandler


class General_conf:
    role = ['admin', 'editor', 'user']


class app_conf:
    app = Flask(__name__)
    CORS(app, supports_credentials=True)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://postgres:postgres@127.0.0.1:5432/smm')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['SESSION_FILE_DIR'] = '/tmp/flask_session'
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.config['SESSION_COOKIE_SECURE'] = False  # Set to True in production with HTTPS
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
    app.config['SECRET_KEY'] = 'your-secret-key'  # Секретный ключ для подписи сессий


class redis_conf:
    redis_host = os.getenv('REDIS_HOST', 'redis')
    redis_port = int(os.getenv('REDIS_PORT', 6379))
    redis_db = int(os.getenv('REDIS_DB', 1))
    redis_client = redis.StrictRedis(host=redis_host, port=redis_port, db=redis_db)

    # app_conf.app.config['CACHE_TYPE'] = 'redis'
    # app_conf.app.config['CACHE_REDIS'] = redis_client

    app_conf.app.config['CACHE_TYPE'] = 'RedisCache'
    app_conf.app.config['CACHE_REDIS_HOST'] = redis_host
    app_conf.app.config['CACHE_REDIS_PORT'] = redis_port
    app_conf.app.config['CACHE_REDIS_DB'] = redis_db

    cache = Cache(app_conf.app)


class boto3_conf:
    S3_BUCKET_NAME = 'bucket-de6ad0'
    session = boto3.session.Session(profile_name='default')
    s3_client = session.client(
        service_name='s3',
        endpoint_url='https://s3.cloud.ru'
    )   

class rabbitmq_conf:
    connection_params = ConnectionParameters(
        host=os.getenv('RABBITMQ_HOST', '127.0.0.1'),
        port=int(os.getenv('RABBITMQ_PORT', 5672))
    )

class logging_conf:
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    logger = logging.getLogger(__name__)