from flask import Blueprint
# from .index import index_bp
from .user.auth import auth_bp
from .user.profile import profile_bp
from .user.users import users_bp
from .post.create_post import posts_bp
from .post.posts import get_posts_bp
from .post.post_edit import edit_post_bp
from .post.delete_post import del_post_bp

def register_routes(app):
    # app.register_blueprint(index_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(profile_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(posts_bp)
    app.register_blueprint(get_posts_bp)
    app.register_blueprint(edit_post_bp)
    app.register_blueprint(del_post_bp)

