from pika import BlockingConnection
import json
from config import rabbitmq_conf, app_conf
from models import db
from models.channel import Channel

def callback(ch, method, properties, body: str) -> None:
    data: json

    try:
        data = json.loads(body)
        if data.get('action') == 'add':

            tg_id = data.get('tg_id')
            name = data.get('name')
            user_name = data.get('user_name')

            channel = Channel(tg_id=tg_id, name=name, user_name=user_name)
            db.session.add(channel)
            db.session.commit()

            print(f"Добавлен канал: {user_name} ({tg_id})")
        
        elif data.get('action') == 'kicked':
            tg_id = data.get('tg_id')
            channel = db.session.query(Channel).filter_by(tg_id=tg_id)
            channel.delete()
            db.session.commit()
        
    except Exception as e:
        print(f"Ошибка при обработке {e}")

def get_tg():
    with app_conf.app.app_context():
        with BlockingConnection(rabbitmq_conf.connection_params) as conn:
            ch = conn.channel()
            ch.queue_declare(queue='chenal_status_new', durable=True)

            ch.basic_consume(
                queue='chenal_status_new',
                on_message_callback=callback,
                auto_ack=True
            )

            print("Ожидание сообщений...")
            ch.start_consuming()
