import datetime
from models import db


class Media(db.Model):
    __tablename__ = 'media'

    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    s3_key = db.Column(db.String(1024), nullable=False, unique=True)
    mime_type = db.Column(db.String(100))
    uploaded_at = db.Column(db.DateTime, default=datetime.time)

    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=True)