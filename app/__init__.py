import os
from dotenv import load_dotenv
from flask import Flask
from app.extensions import db, migrate, login_manager
from app.models import User

# Load environment variables from .env files.
load_dotenv()


# Function to create the Flask application.
def create_app():
    app = Flask(__name__)

    # Use environment variables.
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
        'SQLALCHEMY_DATABASE_URI')
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    # Redirect unauthorized users to login
    login_manager.login_view = "main.login"
    login_manager.login_message = "Please log in to access this page."
    login_manager.login_message_category = "info"

    # Register blueprints or routes
    from app.routes import main
    app.register_blueprint(main)

    return app


# Function to load user to the application.
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
