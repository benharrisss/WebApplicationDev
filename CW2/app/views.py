from flask import render_template, flash, redirect, url_for, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from app import app, db
from datetime import datetime
from .models import User, Post, Reply
from .forms import LoginForm, RegisterForm, CreatePostForm, ReplyForm, ChangePasswordForm
import json


# Route to handle user registration
@app.route('/register', methods=['GET', 'POST'])
def register():
   # Redirect to home page if user is already logged in
   if current_user.is_authenticated:
      return redirect(url_for('index'))
   form = RegisterForm()
   # Server-side validation for register form
   if form.validate_on_submit():
      # Check if username or email is already registered
      existing_user = User.query.filter((User.username == form.username.data) | (User.email == form.email.data)).first()
      if existing_user:
         # Check if username or email is already taken
         if existing_user.email == form.email.data:
            flash('Email is already registered.', 'danger')
            return redirect(url_for('register'))
         elif existing_user.username == form.username.data:
            flash('This username is already taken.', 'danger')
            return redirect(url_for('register'))
      # Create a new user
      user = User(username=form.username.data, email=form.email.data)
      # Hash password
      user.set_password(form.password.data)
      # Add and commit changes to database
      db.session.add(user)
      db.session.commit()
      flash('Registration complete! You may now log in.', 'success')
      # Redirect to login page
      return redirect(url_for('login'))
   return render_template('register.html', form=form)
   
# Route to handle user login
@app.route('/login', methods=['GET', 'POST'])
def login():
   # Redirect to home page if user is already logged in
   if current_user.is_authenticated:
      return redirect(url_for('index'))
   form = LoginForm()
   # Server-side validation for login form
   if form.validate_on_submit():
      # Query user by ther username
      user = User.query.filter_by(username=form.username.data).first()
      # Check if password matches stored password
      if user and user.check_password(form.password.data):
         # Log the user in
         login_user(user)
         flash('Successfully logged in!', 'success')
         # Redirect to home page
         return redirect(url_for('index'))
      flash('Incorrect username or password.', 'danger')
   return render_template('login.html', form=form)
   
# Route to handle user logout
@app.route('/logout')
@login_required
def logout():
   # log the user out
   logout_user()
   flash('You have been logged out.', 'info')
   # Redirect to login page
   return redirect(url_for('login'))
   
# Route to display newest posts
@app.route('/newest_posts', methods=['GET'])
def newest_posts():
   # Get all posts ordered by post date
   posts = Post.query.order_by(Post.post_date.desc()).all()
   liked_posts = [post.id for post in posts if current_user in post.user_likes]
   return render_template('view_posts.html', posts=posts, liked_posts=liked_posts, filter="new")
   
# Route to display top posts
@app.route('/top_posts', methods=['GET'])
def top_posts():
   # Get all posts ordered by like count
   posts = Post.query.order_by(Post.likes_count.desc()).all()
   liked_posts = [post.id for post in posts if current_user in post.user_likes]
   return render_template('view_posts.html', posts=posts, liked_posts=liked_posts, filter="top")
   
# Route to view a single post and its replies
@app.route('/view_post/<int:post_id>', methods=['GET', 'POST'])
def view_post(post_id):
   post = Post.query.get_or_404(post_id)
   form = ReplyForm()
   # Server-side validation for reply form
   if form.validate_on_submit():
      # Add reply to the post
      reply = Reply(content=form.content.data, post=post, author=current_user)
      # Add and commit changes to database
      db.session.add(reply)
      db.session.commit()
      flash('Reply added!', 'success')
      # Redirect to the specific post
      return redirect(url_for('view_post', post_id=post_id))
   return render_template('view_post.html', post=post, post_id=post_id, form=form)
   
# Route to create a new post
@app.route('/create_post', methods=['GET', 'POST'])
@login_required
def create_post():
   form = CreatePostForm()
   # Server-side validation for creating a post
   if form.validate_on_submit():
      # Create new post with form data
      post = Post(title=form.title.data, content=form.content.data, user_id=current_user.id)
      # Add and commit changes to database
      db.session.add(post)
      db.session.commit()
      flash('Post created!', 'success')
      # Redirect to newest posts to see their new post
      return redirect(url_for('newest_posts'))
   return render_template('create_post.html', form=form)
   
# Route to add a reply to a post
@app.route('/reply/<int:post_id>', methods=['POST'])
@login_required
def reply(post_id):
   # Request reply content 
   content = request.form.get('content')
   # Checking if reply is empty
   if not content:
      flash('Reply cannot be empty.', 'danger')
      return redirect(url_for('newest_posts', post_id=post_id))
   post = Post.query.get_or_404(post_id)
   # Create new reply to post
   reply = Reply(content=content, post=post, author=current_user)
   # Add and commit changes to database
   db.session.add(reply)
   db.session.commit()
   flash('Reply added!', 'success')
   # Redirect to the specific post
   return redirect(url_for('view_post', post_id=post_id))
   
# Route to handle liking and unliking 
@app.route('/likes/<int:post_id>', methods=['POST'])
@login_required
def like_post(post_id):
   post = Post.query.get_or_404(post_id)
   # Parse JSON data from request
   data = request.get_json()
   # Get like or unlike action
   action = data.get('action')
      
   # Update like status based on like or unlike action
   if action == "like":
      if current_user not in post.user_likes:
         post.user_likes.append(current_user)
         post.likes_count += 1
   elif action == "unlike":
      if current_user in post.user_likes:
         post.user_likes.remove(current_user)
         post.likes_count -= 1
   
   # Commit changes to database
   db.session.commit()
   return jsonify(success=True, like_count=post.likes_count)
   
# Route to display a user's profile
@app.route('/profile')
@login_required
def profile(): 
   # Query posts, replies and liked posts of the current user
   user_posts = Post.query.filter_by(user_id=current_user.id).order_by(Post.post_date.desc()).all()
   user_replies = Reply.query.filter_by(user_id=current_user.id).order_by(Reply.post_date.desc()).all()
   liked_posts = current_user.liked_posts
   return render_template('profile.html', user=current_user, posts=user_posts, replies=user_replies, likes=liked_posts)
   
# Route to change user's password
@app.route('/profile/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
   form = ChangePasswordForm()
   # Server-side validation for change password form
   if form.validate_on_submit():
      # Check if current password matches stored password
      if not current_user.check_password(form.current_password.data):
         flash('Current password is incorrect.', 'danger')
         return redirect(url_for('change_password'))
      # Set new password
      current_user.set_password(form.new_password.data)
      # Commit changes to database
      db.session.commit()
      flash('Password successfully updated!', 'success')
      # Redirect to profile
      return redirect(url_for('profile'))
   return render_template('change_password.html', form=form)
   
# Route to home page
@app.route('/')
def index():
   return render_template('index.html', filter="home")   


