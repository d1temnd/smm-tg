from flask import Blueprint, request, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_session import Session
from models.user import User
from models import db
from utils.is_role import role_required

users_bp = Blueprint('users', __name__, url_prefix='/api/admin')


@users_bp.route('/users', methods=['GET'])
@role_required('admin')
def get_users():
    users = db.session.query(User).all()

    response = [
        {
            'id': user.id,
            'name': user.name,
            'rule': user.rule

        }
        for user in users
    ]

    return jsonify(response)


@users_bp.route('/user/<int:id>', methods=['GET'])
@role_required('admin')
def get_user(id):
    user = db.session.query(User).filter_by(id=id).first()

    return jsonify({'id': user.id, 'name': user.name, 'rule': user.rule})

