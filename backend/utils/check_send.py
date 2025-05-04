import base64
from time import time, sleep
from models.post import Post
from models import db
from config import logging_conf, app_conf
from utils.s3 import get_file_s3
from models.media import Media
from broker.producer import send_message
from models.channel import Channel

def send_post(post):
    print(f"Отправка поста {post.id}")
    with app_conf.app.app_context():
        media = post.preview_image  # используем relationship, а не query
        channel = Channel.query.filter_by(id=post.chanal_id).first()
        
        if media is None:
            print(f"Внимание: для поста {post.id} не найдено превью-медиа")
            send_message({
                'chat_id': channel.tg_id,
                'message': post.text,
                'file': None
            })
            return

        file = get_file_s3(media.s3_key)
        encoded_file = base64.b64encode(file).decode('utf-8')
        print(encoded_file)

        send_message({
            'chat_id': channel.tg_id,
            'message': post.text,
            'file': encoded_file, 
            'media_id': media.id
        })


def check_send_loop():
    while True:
        with app_conf.app.app_context():  # Ensure the code is within the app context
            current_time = int(time())
            posts_to_send = db.session.query(Post).filter(
                Post.time_publication <= current_time,
                Post.status == False
            ).all()

            # logging_conf.logger.info(f"Текущее время: {current_time}, Найдены посты для отправки: {len(posts_to_send)}, {[(p.id, p.time_publication) for p in posts_to_send]}")

            for post in posts_to_send:
                send_post(post)
                post.status = True

            db.session.commit()
        sleep(5)
