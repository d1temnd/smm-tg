import uuid
from flask import Blueprint, request, jsonify, session
from datetime import datetime
from models import db
from models.post import Post
from models.media import Media
from models.channel import Channel  # Добавлена модель Channel
from config import boto3_conf
from utils.is_role import role_required
from utils import s3



posts_bp = Blueprint('posts', __name__, url_prefix='/api/post')

@posts_bp.route('/create', methods=['POST'])
@role_required('admin', 'editor')
def create_post():
    # Получаем данные из формы
    text = request.form.get('text')
    chanal_id = request.form.get('chanal_id')
    file = request.files.get('file')

    # Проверка наличия обязательных данных
    if not text or not chanal_id:
        return jsonify({'error': 'Missing text or channel ID'}), 400

    # Проверка наличия канала с таким ID
    channel = Channel.query.get(chanal_id)
    if not channel:
        return jsonify({'error': 'Channel not found'}), 404

    file_url = None
    if file:
        # Проверка на тип файла
        if not file.content_type.startswith('image'):
            return jsonify({'error': 'Invalid file type. Only images are allowed.'}), 400

        try:

            filename = f"{uuid.uuid4().hex}_{file.filename}"
            
            file_url = s3.upload_s3(file, filename)
        except Exception as e:
            return jsonify({'error': f'File upload failed: {str(e)}'}), 500

    # Создание записи в таблице Post
    post = Post(
        autor_id=session['user_id'],
        text=text,
        chanal_id=chanal_id, 
        image_path=file_url
    )
    db.session.add(post)
    db.session.commit()

    if file_url:
        media = Media(
        filename=file.filename,
        s3_key=filename,
        mime_type=file.content_type,
        uploaded_at=datetime.utcnow(),
        post_id=post.id
        )

        db.session.add(media)
        db.session.commit()

    return jsonify({'message': 'Post created successfully', 'post_id': post.id})
