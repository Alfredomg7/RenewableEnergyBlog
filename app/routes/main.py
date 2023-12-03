# Import necessary modules and packages
from flask import flash, render_template, url_for, request, redirect
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import current_user, login_user, logout_user, login_required
from app import app, db
from app.models import Article, Message, User

# Route for the homepage
@app.route('/')
def index():
    articles = Article.query.all()
    return render_template('index.html', articles=articles)

# Route for the 'About' page
@app.route('/about')
def about():
    return render_template('about.html')

# Route for the contact form, handling both display (GET) and data submission (POST)
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        # Extract data from the contact form
        sender = request.form.get('name')
        email = request.form.get('email')
        title = request.form.get('title')
        message = request.form.get('message')
        priority = request.form.get('priority')

        # Create a new message record and save it to the database
        new_message = Message(sender=sender, email=email, title=title, message=message, priority=priority)
        db.session.add(new_message)
        db.session.commit()

        # Notify the user of successful message submission
        flash("Message sent. Thanks for reaching out!")
        return redirect(url_for('index'))
    
    # Render the contact form template on GET request
    return render_template('contact.html')

# Route for handle user registration
@app.route('signup', methods=['GET', 'POST'])
def register():
    # Handle POST request: user registration
    if request.method == "POST":
        # Extract user details from form data
        username = request.form.get('username')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        password = request.form.get('password')

        # Check if username already exists in the database
        username_exists = User.query.filter_by(username=username).first()
        if username_exists:
            flash("This username already exists.")
            return redirect(url_for('register'))
        
        # Check if email is already registered
        email_exists = User.query.filter_by(email=email).first()
        if email_exists:
            flash("This email is already registered.")
            return redirect(url_for('register'))
        
        # Hash the password for security
        password_hash = generate_password_hash(password)

        # Create new user record
        new_user = User(username=username, first_name=first_name,
                        last_name=last_name, email=email,
                        password_hash=password_hash)
        
        # Add the new user to the database
        db.session.add(new_user)
        db.session.commit()

        # Notify the user of succesful registration
        flash("You are now signed up.")
        return redirect(url_for('login'))
    
    # Render the signup template on GET request
    return render_template('signup.html')

# Route for handle user login
@app.route('login', methods=['GET', 'POST'])
def login():
    # Check if the request method is POST (form submission)
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Query the database for the user
        user = User.query.filter_by(username=username).first()

        # Check if user exists and password is correct
        if user and check_password_hash(user.password_hash, password):
            # Log in the user and redirect to the index page
            login_user(user)
            flash("You are now logged in.")
            return redirect(url_for('index'))
    
        # If user does not exist or password is incorrect
        else:
            flash("Username or Password not valid.")
            return redirect(url_for('login'))
    
    # Render the login template if method is GET or credentials are invalid
    return render_template('login.html')