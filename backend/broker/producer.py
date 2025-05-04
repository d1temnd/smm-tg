import json
from pika import BlockingConnection
from config import rabbitmq_conf


def send_message(message: dict):
    with BlockingConnection(rabbitmq_conf.connection_params) as conn:
        ch = conn.channel()
        ch.queue_declare(queue='send_post', durable=True)

        ch.basic_publish(
            exchange='',
            routing_key='send_post',
            body=json.dumps(message),
            properties=None
        )
