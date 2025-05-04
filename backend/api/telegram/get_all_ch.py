from flask import Blueprint, request, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_session import Session
from models.user import User
from models.post import Post
from models.channel import Channel
from models import db
from utils.is_role import role_required

get_ch_bp = Blueprint('get_ch', __name__, url_prefix='/api/telegram')


@get_ch_bp.route('/all', methods=['GET'])
@role_required('admin', 'editor')
def get_ch():
    ch = db.session.query(Channel).all()
    

    response = [
    {
        'id': chanal.id,
        'tg_id': chanal.tg_id,
        'user_name': '@' + chanal.user_name if chanal.user_name else 'None',
        'name': chanal.name
    }
    for chanal in ch
    ]

    return jsonify(response), 200
