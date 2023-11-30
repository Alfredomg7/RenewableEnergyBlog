"""Blog Platform Flask Application"""

# Import necesary libraries
from flask import Flask, flash, render_template, url_for, request, redirect
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
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///' + os.path.join(base_dir, 'renewable_energy_blog.db')
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

# Define 'Message' class to store contact form messages in the 'messages' table
class Message(db.Model):
    __tablename__ = "messages"
    id = db.Column(db.Integer, primary_key=True)
    sender = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(80), nullable=False)
    title = db.Column(db.String(80), nullable=False)
    message = db.Column(db.String, nullable=False)
    priority = db.Column(db.String(20))

    def __repr__(self):
        return f"Message: <{self.title}>"
    
# Initialize and create database tables from models if they don't already exist
@app.before_first_request
def create_tables():
    db.create_all()

# Define route for the homepage, displaying a list of articles
@app.route('/')
def index():
    articles = Article.query.all()
    context = {
        "articles": articles
    }
    return render_template('index.html', **context)

# Route definition for the 'About' page
@app.route('/about')
def about():
    return render_template('about.html')

# Define route for contact form, handling both display (GET) and data submission (POST)
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        # Extracting data from the contact form
        sender = request.form.get('name')
        email = request.form.get('email')
        title = request.form.get('title')
        message = request.form.get('message')
        priority = request.form.get('priority')

        # Creating a new message record and saving it to the database
        new_message = Message(sender=sender, email=email,
                                title=title, message=message,
                                priority=priority)
        db.session.add(new_message)
        db.session.commit()

        # Notification for successful message submission
        flash("Message sent. Thanks for reaching out!")
        return redirect(url_for('index'))
    
    # Render the contact form template on GET request
    return render_template('contact.html')