from functools import wraps
from flask import session, jsonify
from werkzeug.exceptions import Forbidden, Unauthorized
from models.user import User

def role_required(*allowed_roles):
    """
    Декоратор, разрешающий доступ только пользователям с одной из указанных ролей.
    Пример: @role_required('admin', 'editor')
    """
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            user_id = session.get('user_id')
            if not user_id:
                # Если не залогинен
                raise Unauthorized("Authentication required")
            
            user = User.query.get(user_id)
            if not user:
                # Пользователь не найден в БД
                raise Unauthorized("Invalid session")
            
            if user.rule not in allowed_roles:
                # Роль есть, но не в списке разрешённых
                raise Forbidden(f"Role '{user.rule}' is not allowed")
            
            # Всё ок: передаём управление основному обработчику
            return f(*args, **kwargs)
        return wrapped
    return decorator
