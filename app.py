"""Blog Platform Flask Application"""

# Import necesary libraries
from flask import Flask, flash, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

# Initialize Flask application
app = Flask(__name__)

# Load the environment variables from the .env file
load_dotenv()  

# Configure the database connection
base_dir = os.path.dirname(os.path.realpath(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///' + os.path.join(base_dir, 'renewable_energy_blog.db')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = os.getenv('SECRET_KEY')

# Initialize database
db = SQLAlchemy(app)

# Import models
from models import User, Article, Message
    
# Define function to initialize database creating the tables
def create_tables():
    with app.app_context():
        db.create_all()

# Call the function to create database tables
create_tables()

# Initialize database tables at app startup
@app.route('/')
def index():
    articles = Article.query.all()
    context = {
        "articles": articles
    }
    return render_template('index.html', **context)

# Define route for the 'About' page
@app.route('/about')
def about():
    return render_template('about.html')

# Define route for contact form, handling both display (GET) and data submission (POST)
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        # Extract data from the contact form
        sender = request.form.get('name')
        email = request.form.get('email')
        title = request.form.get('title')
        message = request.form.get('message')
        priority = request.form.get('priority')

        # Create a new message record and saving it to the database
        new_message = Message(sender=sender, email=email,
                                title=title, message=message,
                                priority=priority)
        db.session.add(new_message)
        db.session.commit()

        # Notify for successful message submission
        flash("Message sent. Thanks for reaching out!")
        return redirect(url_for('index'))
    
    # Render the contact form template on GET request
    return render_template('contact.html')