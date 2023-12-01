# Import necessary modules and packages
from flask import render_template, request, redirect, url_for, flash
from app import app, db
from app.models import Article, Message

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
