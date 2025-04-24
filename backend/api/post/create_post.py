# api/posts.py
import uuid
from flask import Blueprint, request, jsonify, session
from models import db
from models.post import Post
from models.media import Media
from config import minio_conf

posts_bp = Blueprint('posts', __name__, url_prefix='/api/posts')

@posts_bp.route('/create', methods=['POST'])
def create_post():
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401

    text = request.form.get('text')
    chanal_id = request.form.get('chanal_id')
    file = request.files.get('file')

    if not text or not chanal_id:
        return jsonify({'error': 'Missing data'}), 400

    # Загружаем файл в MinIO
    file_url = None
    if file:
        bucket_name = "bucket-de6ad0"
        if not minio_conf.minio_client.bucket_exists(bucket_name):
            minio_conf.minio_client.make_bucket(bucket_name)
        filename = f"{uuid.uuid4()}_{file.filename}"
        minio_conf.minio_client.put_object(
            bucket_name,
            filename,
            file.stream,
            length=-1,
            part_size=10*1024*1024,
            content_type=file.mimetype
        )
        file_url = f"https://s3.cloud.ru/{bucket_name}/{filename}"  # Заменить на публичный URL

    post = Post(
        autor_id=session['user_id'],
        text=text,
        chanal_id=chanal_id
    )
    db.session.add(post)
    db.session.commit()

    if file_url:
        media = Media(
            path=file_url,
            post_id=post.id
        )
        db.session.add(media)

    db.session.commit()

    return jsonify({'message': 'Post created successfully', 'post_id': post.id})
