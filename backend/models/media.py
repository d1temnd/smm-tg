import time
from models import db

class Media(db.Model):
    __tablename__ = 'media'

    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String, nullable=False)
    s3_key = db.Column(db.String, nullable=False)
    mime_type = db.Column(db.String)
    uploaded_at = db.Column(db.BigInteger)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))  # обычная связь
