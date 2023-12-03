# Import necessary modules
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from dotenv import load_dotenv
import os

# Load enviroment variables from .env file
load_dotenv()

# Initialize the Flask application
app = Flask(__name__)

# Configure the application settings
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///' + os.path.join(os.path.dirname(os.path.realpath(__file__)), 'renewable_energy_blog.db')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = os.getenv('SECRET_KEY')

# Initialize SQLAlchemy with the Flask application
db = SQLAlchemy(app)

# Initialize Login Manager
login_manager = LoginManager(app)

# Import model
from app.models import User, Article, Message

# Create the database tables
with app.app_context():
    db.create_all()
    
# Import route handlers from
from app.routes import main

# User loader function for LoginManager
@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))
