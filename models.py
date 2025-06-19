"""
Database models for Kira-Blog.
Defines User and Post models and their relationships.
"""

from extensions import db
from datetime import datetime

class User(db.Model):
    """
    User model for authentication and post ownership.

    Fields:
        id (int): Primary key.
        username (str): Unique username.
        email (str): Unique email address.
        password (str): Hashed password.
        posts (list): Relationship to Post.
    """

    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)

    posts = db.relationship('Post', back_populates='author')

class Post(db.Model):
    """
    Post model for blog posts.

    Fields:
        id (int): Primary key.
        title (str): Post title.
        content (str): Post content.
        created_at (datetime): Timestamp.
        user_id (int): Foreign key to User.
        author (User): Relationship to User.
    """

    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    author = db.relationship('User', back_populates='posts')
