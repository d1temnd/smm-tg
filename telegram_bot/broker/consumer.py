from pika import BlockingConnection
import json
from config import rabbitmq_conf, bot_conf
import base64
from utils import escape_markdown_v2


def callback(ch, method, properties, body):
    message = json.loads(body)
    # print(f"Получено сообщение: {message}, {type(message)}")
    # print(f'{message.get('test')}')
    chat_id = message.get('chat_id')
    mgs = escape_markdown_v2(message.get('message'))
    file = message.get('file')
    media_id = message.get('media_id')

    print(f"Получено сообщение: {message}, {type(message)}")

    if file:
        file = base64.b64decode(file)
        bot_conf.bot.send_photo(chat_id=chat_id, photo=file, caption=mgs, parse_mode='MarkdownV2')
    else:
        bot_conf.bot.send_message(chat_id=chat_id, text=mgs, parse_mode='MarkdownV2')


def get_post():
    with BlockingConnection(rabbitmq_conf.connection_params) as conn:
        ch = conn.channel()
        ch.queue_declare(queue='send_post', durable=True)

        ch.basic_consume(
            queue='send_post', 
            on_message_callback=callback,
            auto_ack=True  # чтобы сообщения автоматически помечались как "прочитанные"
        )

        print("Ожидание сообщений...")
        ch.start_consuming()

