from flask import Flask
from models import db
from models.user import User  # Явно импортируем модели
from models.channel import Channel
from models.post import Post
from models.media import Media
from api import register_routes

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://myuser:mypassword@localhost:5432/smm'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SECRET_KEY'] = 'your-secret-key'  # Секретный ключ для подписи сессий

db.init_app(app)
register_routes(app)

if __name__ == '__main__':
    with app.app_context():
        
        db.create_all()
        print("Таблицы созданы:", list(db.metadata.tables.keys()))
    
    app.run(debug=True, host="0.0.0.0")