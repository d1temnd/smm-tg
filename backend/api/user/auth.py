from flask import Blueprint, request, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_session import Session
from models.user import User
from models import db

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    if not data.get('name') or not data.get('password'):
        return jsonify({'error': 'Missing username or password'}), 400

    if User.query.filter_by(name=data['name']).first():
        return jsonify({'error': 'User already exists'}), 400

    user = User(name=data['name'], rule='admin')
    user.set_password(data['password'])

    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'User registered successfully'}), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(name=data.get('name')).first()

    if user and user.check_password(data.get('password')):
        # Создаём сессию для пользователя
        session['user_id'] = user.id
        session['username'] = user.name
        return jsonify({'message': 'Login successful'})
    
    return jsonify({'error': 'Invalid credentials'}), 401


@auth_bp.route('/logout', methods=['POST'])
def logout():
    session.clear()  # Удаляем сессию
    return jsonify({'message': 'Logged out successfully'})


