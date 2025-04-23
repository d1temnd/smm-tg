from models import db


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    rule = db.Column(db.String(50), nullable=False)

    posts = db.relationship('Post', backref='author', lazy=True)