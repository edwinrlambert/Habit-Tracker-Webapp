from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

# Initialize database variables.
db = SQLAlchemy()
migrate = Migrate()

# initialize login manager.
login_manager = LoginManager()
