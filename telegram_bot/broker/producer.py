import json
from pika import BlockingConnection
from config import rabbitmq_conf


def send_add_ch(message: dict):
    '''
    Отправляет сообщение в очередь "chenal_status".

    Пример message:
    {
        "tg_id": -1002578002, 
        "name": "real_32t", 
        "user_name": "@t2est"
    }
    '''
    with BlockingConnection(rabbitmq_conf.connection_params) as conn:
        ch = conn.channel()
        ch.queue_declare(queue='chenal_status_new', durable=True)

        ch.basic_publish(
            exchange='',
            routing_key='chenal_status_new',
            body=json.dumps(message),
            properties=None  # можно сюда добавить delivery_mode=2 для персистентности
        )
