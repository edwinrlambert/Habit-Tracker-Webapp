import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv

# Load environment variables from .env files.
load_dotenv()

# Initialize database variables.
db = SQLAlchemy()
migrate = Migrate()


def create_app():
    app = Flask(__name__)

    # Use environment variables.
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
        'SQLALCHEMY_DATABASE_URI')
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # Register blueprints or routes
    from app.routes import main
    app.register_blueprint(main)

    return app
