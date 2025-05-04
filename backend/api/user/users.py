from flask import Blueprint, request, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_session import Session
from models.user import User
from models import db
from utils.is_role import role_required
from config import General_conf

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



@users_bp.route('/<int:id>/role', methods=['PUT'])
@role_required('admin')
def change_role(id):
    data = request.json
    new_role = data.get('new_role')

    if not new_role:
        return jsonify({'error': 'Missing new_role'}), 400
    
    if new_role not in General_conf.role:
        return jsonify({'error': 'Invalid role'}), 400
    
    user = db.session.query(User).filter_by(id=id).first()

    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    user.rule = new_role
    db.session.commit()

    return jsonify({'success': True, 'user_id': user.id, 'new_role': new_role})


@users_bp.route('/user/delete', methods=['DELETE'])
@role_required('admin')
def delete_user():
    data = request.json
    user_id = data.get('id')

    user = db.session.query(User).filter_by(id=user_id).first()

    if not user:
        return jsonify({'error': 'User not found'}), 404

    db.session.delete(user)
    db.session.commit()

    return jsonify({'message': 'User deleted successfully', 'user_id': user.id})
