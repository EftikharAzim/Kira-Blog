"""
Kira-Blog Flask Application Factory

This module provides the create_app function to initialize the Flask app,
register extensions, and set up blueprints for the API.
"""

from flask import Flask
from config import Config
from extensions import db, jwt
from flask_cors import CORS
from flask_restx import Api

def create_app():
    """
    Application factory for Kira-Blog.
    Initializes Flask app, configures extensions, registers blueprints, and creates database tables.
    
    Returns:
        app (Flask): The configured Flask application instance.
    """
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    jwt.init_app(app)
    CORS(app)  # Enable CORS for all routes

    api = Api(app, doc='/docs', title='Kira-Blog API', description='API documentation for Kira-Blog')

    from routes.auth import auth_bp
    from routes.posts import posts_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(posts_bp)

    from error_handlers import register_error_handlers
    register_error_handlers(app)

    with app.app_context():
        db.create_all()

    return app
