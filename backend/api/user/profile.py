from flask import Blueprint, request, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_session import Session
from models.user import User
from models import db

profile_bp = Blueprint('profile', __name__, url_prefix='/api/auth')


@profile_bp.route('/profile', methods=['GET'])
def profile():
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401

    user = User.query.get(session['user_id'])
    return jsonify({'user': {'id': user.id, 'name': user.name, 'rule': user.rule}})