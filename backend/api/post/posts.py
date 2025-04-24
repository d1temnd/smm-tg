from flask import Blueprint, request, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_session import Session
from models.user import User
from models.post import Post
from models import db
from utils.is_role import role_required

get_posts_bp = Blueprint('get_posts', __name__, url_prefix='/api/post')


@get_posts_bp.route('/all', methods=['GET'])
@role_required('admin', 'editor')
def get_posts():
    posts = db.session.query(Post).all()
    

    response = [
    {
        'id': post.id,
        'autor_name': db.session.query(User).filter_by(id=post.autor_id).first().name,
        'text': post.text,
        'image_path': post.image_path,
        'time_publication': post.time_publication,
        'chanal_id': post.chanal_id
    }
    for post in posts
    ]

    return jsonify(response)


@get_posts_bp.route('/post/<int:id>', methods=['GET'])
@role_required('admin', 'editor')
def get_post(id):
    post = db.session.query(Post).filter_by(id=id).first()
    
    if not post:
        return jsonify({'error': 'Post not found'}), 404

    autor = db.session.query(User).filter_by(id=post.autor_id).first()

    
    return jsonify({
        'id': post.id,
        'autor_name': autor.name if autor else 'Unknown',
        'text': post.text,
        'image_path': post.image_path,
        'time_publication': post.time_publication,
        'chanal_id': post.chanal_id
    })

