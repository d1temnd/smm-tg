from models import db


class Channel(db.Model):
    __tablename__ = 'channel'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tg_id = db.Column(db.BigInteger, unique=True, nullable=False)
    user_name = db.Column(db.String(255), nullable=True, unique=True)
    name = db.Column(db.String(255), nullable=False)

    posts = db.relationship('Post', backref='channel', lazy=True)