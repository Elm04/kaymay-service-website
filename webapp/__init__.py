# webapp/__init__.py
from flask import Flask
import os
from datetime import datetime
from .extensions import db, mail, login_manager, mail

def create_app():
    app = Flask(__name__)
    
    # Configuration
    app.config.update(
        SECRET_KEY=os.environ.get("SECRET_KEY", "MYSECRET_KEY_PASSWORD_IS_HERE"),
        SQLALCHEMY_DATABASE_URI='sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)), 'blog.db'),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        MAIL_SERVER="smtp-mail.outlook.com",
        MAIL_PORT=587,
        MAIL_USERNAME="kaymaydrc@outlook.com",
        MAIL_PASSWORD="Kay@2024m",
        MAIL_USE_TLS=True,
        MAIL_USE_SSL=False
    )

    # Initialisation des extensions
    db.init_app(app)
    mail.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'

    # Context processor
    @app.context_processor
    def inject_site_config():
        from .models import SiteConfig  # Import local pour éviter les circular imports
        config = SiteConfig.query.first()
        if not config:
            config = SiteConfig(
                company_name="Kaymay Services",
                email="info@kaymayservices.com",
                phone="+243 81 88 48 797",
                address="lubilanshi 407"
            )
            db.session.add(config)
            db.session.commit()
        return {'site_config': config}

    # Enregistrement des blueprints
    from .views import views
    from .auth import auth
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    # Création des tables
    with app.app_context():
        db.create_all()
        
        # Création utilisateur admin si nécessaire
        from .models import User
        from werkzeug.security import generate_password_hash
        if not User.query.filter_by(email="admin@kaymayservices.com").first():
            admin = User(
                email="admin@kaymayservices.com",
                password=generate_password_hash("Admin@Kaymay2024"),
                name="Administrateur",
                is_admin=True
            )
            db.session.add(admin)
            db.session.commit()

    return app