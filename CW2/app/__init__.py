from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
app.config.from_object('config')

# Initialise the LoginManager to handle user sessions and authentication
login_manager = LoginManager(app)
login_manager.login_view = 'login' # Specifies route to login when 

# Enforce CSRF protection
csrf = CSRFProtect()
csrf.init_app(app)

db = SQLAlchemy(app)

migrate = Migrate(app, db)

from app import views, models
from app.models import User

# Define user loader function for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

