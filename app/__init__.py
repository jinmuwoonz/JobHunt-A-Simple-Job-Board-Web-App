# This is __init__.py from the app folder

from flask import Flask # Imports the Flask class from the flask module, which is the core of any Flask application.
from flask_sqlalchemy import SQLAlchemy # Imports SQLAlchemy from flask_sqlalchemy, which is an ORM (Object-Relational Mapping) tool for Flask.
from flask_login import LoginManager # Imports LoginManager from flask_login, which handles user session management for logging in/out.
from flask_migrate import Migrate # Imports Migrate from flask_migrate, which handles database migrations for SQLAlchemy.
from os import path

db = SQLAlchemy() # Initialize the SQLAlchemy database
login_manager = LoginManager() # Creates an instance of LoginManager that will be used to manage user authentication.
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config') # Loads configuration settings from a Config class in the config module (typically config.py).

    db.init_app(app) # Initializes the SQLAlchemy instance with the Flask application.
    migrate.init_app(app, db) # Initializes Flask-Migrate with the Flask application and SQLAlchemy instance for database migrations.
    login_manager.init_app(app) # Initializes the LoginManager with the Flask application.

    # Import models/tables for the database
    from .models import User, Applicant, Employer, Job, JobApplication

    # Imports Blueprint objects from different route modules (auth, jobs, dashboard).
    from app.routes.auth import auth_bp
    from app.routes.jobs import jobs_bp
    from app.routes.dashboard import dashboard_bp
    from app.routes.profile import profile_bp

    # Registers each Blueprint with the Flask application, making their routes available.
    app.register_blueprint(auth_bp)
    app.register_blueprint(jobs_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(profile_bp)

    login_manager.login_view = 'jobs_bp.home' # Redirects to the home page if user is not logged in
    
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id)) # Fetches a user by their ID from the database.

    # Create database tables if they don't exist
    with app.app_context():
        if not database_exists(db.engine.url):
            db.create_all()
            print('✅ Created MySQL database tables')

    return app

from sqlalchemy_utils import database_exists