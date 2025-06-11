# webapp/extensions.py
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mailman import Mail

mail = Mail()
db = SQLAlchemy()
mail = Mail()
login_manager = LoginManager()