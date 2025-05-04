import uuid
from flask import Blueprint, request, jsonify, session
from time import time
from datetime import datetime
from models import db
from models.post import Post
from models.media import Media
from models.channel import Channel
from config import boto3_conf
from utils.is_role import role_required
from utils import s3
from models.user import User

posts_bp = Blueprint('posts', __name__, url_prefix='/api/post')


@posts_bp.route('/create', methods=['POST'])
@role_required('admin', 'editor')
def create_post():
    text = request.form.get('text')
    chanal_id = request.form.get('chanal_id')
    file = request.files.get('file')
    send_post = request.form.get('time')
    send_autor = request.form.get('send_autor', 'false').lower() == 'true'

    if not text or not chanal_id:
        return jsonify({'error': 'Missing text or channel ID'}), 400

    channel = Channel.query.get(chanal_id)
    if not channel:
        return jsonify({'error': 'Channel not found'}), 404

    if send_autor:
        user = User.query.filter_by(id=session['user_id']).first()
        text = f"{text}\n\n Автор: {user.name}"

    media = None
    if file:
        if not file.content_type.startswith('image'):
            return jsonify({'error': 'Invalid file type. Only images are allowed.'}), 400

        try:
            filename = f"{uuid.uuid4().hex}_{file.filename.replace(' ', '')}"
            file_url = s3.upload_s3(file, filename)

            media = Media(
                filename=file.filename.replace(' ', ''),
                s3_key=filename,
                mime_type=file.content_type,
                uploaded_at=int(time()),
            )
            db.session.add(media)
            db.session.flush()

        except Exception as e:
            return jsonify({'error': f'File upload failed: {str(e)}'}), 500

    try:
        delay_seconds = int(send_post)
        send_post_time = int(time()) + delay_seconds
    except (TypeError, ValueError):
        return jsonify({'error': 'Invalid send_post value'}), 400

    try:
        post = Post(
            autor_id=session['user_id'],
            text=text,
            chanal_id=chanal_id,
            image_path=media.id if media else None,
            time_publication=send_post_time
        )
        db.session.add(post)
        db.session.commit()
        return jsonify({'message': 'Post created successfully', 'post_id': post.id})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Failed to create post: {str(e)}'}), 500
