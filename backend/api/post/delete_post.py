from flask import Blueprint, request, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_session import Session
from models.user import User
from models.post import Post
from models import db
from utils.is_role import role_required

del_post_bp = Blueprint('del_post', __name__, url_prefix='/api/post')


@del_post_bp.route('/delete', methods=['DELETE'])
@role_required('admin', 'editor')
def edit_post():
    data = request.json
    post_id = data.get('post_id')

    post = db.session.query(Post).filter_by(id=post_id).first()

    if not post:
        return jsonify({'error': 'Post not found'}), 404

    db.session.delete(post)
    db.session.commit()

    return jsonify({'message': 'Post deleted successfully', 'post_id': post.id})
