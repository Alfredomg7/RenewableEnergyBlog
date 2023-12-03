# Renewable Energy Blog

## Introduction
The Renewable Energy Blog is a Flask-based web application that follows the MVC pattern. It's designed for sharing and discussing insights about renewable energy. This interactive blog allows users to read articles, contribute new content, and engage with the community.

## Project Structure
+ **run.py`:** Entry point of the application.
+ **``app/`:** Main application directory.
+ **`__init__.py`:** Initializes the Flask app, database, and login manager.
+ **`templates/`:** Contains HTML templates.
+ **`static/`:**
    +
**`css/`:** Contains CSS files for styling.
    +
**`images/`:** Directory for storing images.
    +
**`js/`:** JavaScript files for front-end functionality.
+ **`routes/:**
    +
**`main.py`**: Contains all the routes and core logic.
    +
**`__init__.py`**: Initialization module for routes.
models/:
    +
**`user.py`, `article.py`, `message.py:`** Modules for the respective database tables.
    +
**`__init__.py`:** Initialization module for models.
+ **`renewable_energy_blog.db`:** SQLite3 database file.
+ **`requirements.txt`:** Lists all the Python dependencies.
+ **`.gitignore`:** Specifies untracked files to ignore.

## Running the Application Locally

To run the Renewable Energy Blog on your local machine, follow these steps:

1. Ensure Python 3 is installed on your machine.
2. Clone the repository to your local machine.
3. Navigate to the project directory in your terminal.
4. Set up a virtual environment (optional but recommended).
5. Activate the virtual environment.
6. Install the required dependencies with **`pip install -r requirements.txt`**.
7. Initialize the database if running the app for the first time.
8. Start the application by executing **`python3 run.py`**.
9. Access the application through your web browser at **`localhost:5000`**.