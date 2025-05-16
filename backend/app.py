from config import app_conf
from models import db
from models.user import User  # Явно импортируем модели
from models.channel import Channel
from models.post import Post
from models.media import Media
from api import register_routes
from broker.consumer import get_tg
from threading import Thread
from utils.check_send import check_send_loop

db.init_app(app_conf.app)
register_routes(app_conf.app)


def main() -> None:
    with app_conf.app.app_context():
        
        db.create_all()
        print("Таблицы созданы:", list(db.metadata.tables.keys()))
    
    Thread(target=get_tg, daemon=True, name="get_tg").start()
    Thread(target=check_send_loop, daemon=True, name="check_send_loop").start()
    app_conf.app.run(debug=False, host="0.0.0.0")


if __name__ == '__main__':
    main()