from config import app_conf
from models import db
from models.user import User  # Явно импортируем модели
from models.channel import Channel
from models.post import Post
from models.media import Media
from api import register_routes


db.init_app(app_conf.app)
register_routes(app_conf.app)

if __name__ == '__main__':
    with app_conf.app.app_context():
        
        db.create_all()
        print("Таблицы созданы:", list(db.metadata.tables.keys()))
    
    app_conf.app.run(debug=True, host="0.0.0.0")