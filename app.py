"""Blog Platform Flask Application"""

# Import necesary libraries
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from dotenv import load_dotenv
from datetime import datetime
import os

# Initialize Flask application
app = Flask(__name__)

# Load the environment variables from the .env file
load_dotenv()  

# Configure database
base_dir = os.path.dirname(os.path.realpath(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///' + os.path.join(base_dir, 'ze_blog.db')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = os.getenv('SECRET_KEY')

# Initialize database
db = SQLAlchemy(app)
db.init__app(app)

# Define 'User' class to represent the 'users' table in the database
class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(80), nullable=False, unique=True)
    password_hash = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"User <{self.username}>"
    
# Define 'Article' class to represent the 'articles' table in the database
class Article(db.Model):
    __tablename__ = "articles"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    content = db.Column(db.String, nullable=False)
    created_on = db.Column(db.Datetime, default=datetime.now())
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), unique=False, nullable=False)
    author = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f"Article: <{self.title}>"
