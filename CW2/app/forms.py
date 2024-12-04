from flask_wtf import FlaskForm
from wtforms import StringField, DateField, TextAreaField, SubmitField, BooleanField, PasswordField
from wtforms.validators import DataRequired, Length, Email, EqualTo

# Form for user to login into the website
class LoginForm(FlaskForm):
    # DataRequired() ensures that data is inputted into the form
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=30)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')
    
# Form for user to register on the website
class RegisterForm(FlaskForm):
    # DataRequired() ensures that data is inputted into the form
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=30)])
    email = StringField('Email', validators=[DataRequired(), Email()]) # Make sure email is of email format
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')]) # Make sure confirm_password is the same as password
    submit = SubmitField('Register')
    
# Form for user to create a new post
class CreatePostForm(FlaskForm):
    # DataRequired() ensures that data is inputted into the form
    title = StringField('Title', validators=[DataRequired(), Length(max=100)])
    content = TextAreaField('content', validators=[DataRequired(), Length(max=1000)])
    submit = SubmitField('Create Post')
    
# Form for user to reply to a post
class ReplyForm(FlaskForm):
    # DataRequired() ensures that data is inputted into the form
    content = TextAreaField('Content', validators=[DataRequired(), Length(max=100)])
    submit = SubmitField('Reply')
   
# Form for user to change their password 
class ChangePasswordForm(FlaskForm):
    # DataRequired() ensures that data is inputted into the form
    current_password = PasswordField('Current Password', validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm new Password', validators=[DataRequired(), EqualTo('new_password')]) # Make sure confirm_password is the same as password
    submit = SubmitField('Change Password')

