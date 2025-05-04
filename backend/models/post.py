import time
from models import db


class Post(db.Model):
    __tablename__ = 'post'

    id = db.Column(db.Integer, primary_key=True)
    autor_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    text = db.Column(db.Text, nullable=False)
    image_path = db.Column(db.Integer, db.ForeignKey('media.id'))  # это типа preview-картинка
    time_publication = db.Column(db.BigInteger)
    status = db.Column(db.Boolean, default=False)
    chanal_id = db.Column(db.Integer, db.ForeignKey('channel.id'), nullable=False)

    # здесь мы явно укажем foreign_keys
    preview_image = db.relationship(
        'Media',
        foreign_keys=[image_path],
        backref='preview_posts',  # не обязательно, можно убрать
        lazy=True
    )

    media = db.relationship(
        'Media',
        backref='post',
        foreign_keys='Media.post_id',
        lazy=True
    )