import datetime
from models import db


class Post(db.Model):
    __tablename__ = 'post'

    id = db.Column(db.Integer, primary_key=True)
    autor_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    text = db.Column(db.Text, nullable=False)  # Markdown текст
    image_path = db.Column(db.String(1024))  # Устарело, можно не использовать
    time_publication = db.Column(db.DateTime, default=datetime.utcnow)
    chanal_id = db.Column(db.Integer, db.ForeignKey('channel.id'), nullable=False)

    media = db.relationship('Media', backref='post', lazy=True)