from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime

db = SQLAlchemy()  # Initialize SQLAlchemy

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False) # Store the HASH, not the actual password

    def __repr__(self):
        return '<User %r>' % self.username

class Post(db.Model):  # For storing generated posts
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) # Foreign Key for the User
    title = db.Column(db.Text, nullable=False, default="No Title!") # Store the title for the generated post
    content = db.Column(db.Text, nullable=False) # Store the generated post content
    generated_post = db.Column(db.Text, nullable=False) # Store the generated post
    platform = db.Column(db.Text, nullable=True) # Store the platform
    tone_and_style = db.Column(db.Text, nullable=True) # Store the requested tone_&_style
    created_at = db.Column(db.DateTime, default=datetime.utcnow) # Timestamp

    def __repr__(self):
        return '<Post %r>' % self.content[:50] # Display a snippet of the content