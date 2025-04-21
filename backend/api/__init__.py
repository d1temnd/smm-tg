from flask import Blueprint
from .index import index_bp

def register_routes(app):
    app.register_blueprint(index_bp)
