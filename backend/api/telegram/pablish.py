from flask import Blueprint, request, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_session import Session
from models.user import User
from models.post import Post
from models.channel import Channel
from models import db
from utils.is_role import role_required
from time import time


publish_bp = Blueprint('publish', __name__, url_prefix='/api/telegram')


@publish_bp.route('/publish/<int:post_id>', methods=['POST'])
@role_required('admin', 'editor')
def publish(post_id):
    post = db.session.query(Post).filter_by(id=post_id).first()

    post.time_publication = int(time())
    db.session.commit()
    

    return jsonify({'message': 'Post published successfully'}), 200
