from flask import Blueprint, request, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_session import Session
from models.user import User
from models.post import Post
from models import db
from utils.is_role import role_required

edit_post_bp = Blueprint('edit_post', __name__, url_prefix='/api/post')


@edit_post_bp.route('/edit', methods=['PUT'])
@role_required('admin', 'editor')
def edit_post():
    data = request.json
    post_id = data.get('id')
    new_text = data.get('text')
    new_chanal_id = data.get('chanal_id')

    if not post_id:
        return jsonify({'error': 'Post ID is required'}), 400

    post = db.session.query(Post).filter_by(id=post_id).first()
    if not post:
        return jsonify({'error': 'Post not found'}), 404

    # Обновляем поля, если переданы
    if new_text:
        post.text = new_text
    if new_chanal_id:
        post.chanal_id = new_chanal_id

    db.session.commit()

    return jsonify({'message': 'Post updated successfully', 'post_id': post.id})
