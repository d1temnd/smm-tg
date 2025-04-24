from flask import Blueprint
# from .index import index_bp
from .user.auth import auth_bp
from .user.profile import profile_bp
from .user.users import users_bp

def register_routes(app):
    # app.register_blueprint(index_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(profile_bp)
    app.register_blueprint(users_bp)
