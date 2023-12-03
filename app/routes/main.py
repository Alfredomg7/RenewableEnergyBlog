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
@app.route('/signup', methods=['GET', 'POST'])
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
@app.route('/login', methods=['GET', 'POST'])
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

# Route for handle user logout
@app.route('/logout')
def logout():
    logout_user()
    flash("You have been logged out.")
    return redirect(url_for('index'))

# Route for displaying a specific article by its ID
@app.route('/article/<int:id>/')
def article(id):
    # Fetch the article from the database or return a 404 error if not found
    article = Article.query.get_or_404(id)

    # Preparing the context to be passed to the template
    context = {
        "article": article
    }

    # Render the article template, passing in the context which includes the article data
    return render_template('article.html', **context)

# Route for creating a new article, accesible only to logged-in users
@app.route('/contribute', methods=['GET', 'POST'])
@login_required
def contribute():
    # Handle form submission for creating a new article
    if request.method == 'POST':
        # Extract article data from the submmited form
        title = request.form.get('title')
        content = request.form.get('content')
        user_id = current_user.id
        author = current_user.username

        # Check if an article with the same title already exists
        title_exists = Article.query.filter_by(title=title).first()
        if title_exists:
            # Inform the user and redirect to the contribute page again
            flash("This article already exists. Please choose a new title.")
            return redirect(url_for('contribute'))
        
        # Create a new Article record
        new_article = Article(title=title, content=content,
                              user_id = user_id, author=author)

        
        # Add the new article to the database
        db.session.add(new_article)
        db.session.commit()

        # Notify the user of successful submission and redirect to the index page
        flash("Thanks for colaborating with Renewable Energy Blog!")
        return redirect(url_for('index'))
    
    # Render the form template for submitting a new article
    return render_template('contribute.html')

# Route to edit an existing article, accessible only to logged-in users
@app.route('/edit/<int:id>/', methods=['GET', 'POST'])
@login_required
def edit(id):
    # Fetch the article from the database or return a 404 error if not found
    article_to_edit = Article.query.get_or_404(id)

    # Check if the current logged-in user is the author of the article
    if current_user.username == article_to_edit.author:
        # Handle form submission for editing the article
        if request.method == 'POST':
            # Update article data with the submitted form data
            article_to_edit.title = request.form.get('title')
            article_to_edit.content = request.form.get('content')

            # Commit the changes to the database
            db.session.commit()

            # Notify the user of successful update and redirect to the article view
            flash("Your changes have been saved.")
            return redirect(url_for('article', id=article_to_edit.id))
        
        # Prepare context with the article data for rendering the edit form
        context = {
            'article': article_to_edit
        }

        # Render the edit template on GET request or if the user is the author
        return render_template('edit.html', **context)
    
    # Notify the user if they are not authorized to edit and redirect to index
    flash("You cannot edit another user's article.")
    return redirect(url_for('index'))
    