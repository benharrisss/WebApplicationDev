from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from app import db

# Association table for many-to-many relationship between User and Post
likes = db.Table('likes', db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True), db.Column('post_id', db.Integer, db.ForeignKey('post.id'), primary_key=True))

# Database for storing User details
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True) # Primary key 
    username = db.Column(db.String(30), unique=True, nullable=False) # Unique username
    email = db.Column(db.String(100), unique=True, nullable=False) # Unique email
    hashed_password = db.Column(db.String(100), nullable=False) # Hash for secure password
    posts = db.relationship('Post', backref='author', lazy=True) # One-to-many relationship
    replies = db.relationship('Reply', backref='author', lazy=True) # One-to-many relationship
    liked_posts = db.relationship('Post', secondary=likes, back_populates='user_likes') # Many-to-many relationship
    
    # Hashes and sets password
    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)
    
    # Verifies password against hashed password
    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)
       
# Database for Posts by a user 
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True) # Primary key
    title = db.Column(db.String(100), nullable=False) # Title of post
    content = db.Column(db.Text, nullable=False) # Content of post
    post_date = db.Column(db.DateTime, default=datetime.utcnow) # Date and time of post
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) # Foreign key linking to user of the post
    replies = db.relationship('Reply', backref='post', lazy=True) # One-to-many relationship
    likes_count = db.Column(db.Integer, default=0) # Tracks number of likes on a post
    user_likes = db.relationship('User', secondary=likes, back_populates='liked_posts') # Many-to-many relationship
    
# Databse for Replies to a post
class Reply(db.Model):
    id = db.Column(db.Integer, primary_key=True) # Primary key
    content = db.Column(db.Text, nullable=False) # Content of reply
    post_date = db.Column(db.DateTime, default=datetime.utcnow) # Date and time of reply
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False) # Foreign key linking to post of the reply
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) # Foreign key linking to user of the reply
    


