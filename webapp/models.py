from datetime import datetime
from .extensions import db, login_manager
from flask_login import UserMixin



about_text ="""
Kaymay Services est votre partenaire de confiance pour tous vos besoins en construction, rénovation et
            design de bâtiments. Notre équipe expérimentée et passionnée s'engage à offrir des services de haute
            qualité, que ce soit pour la construction de nouveaux bâtiments, la rénovation de propriétés existantes ou
            la conception architecturale. Nous mettons l'accent sur l'innovation, la durabilité et la satisfaction du
            client, en veillant à ce que chaque projet reflète vos besoins et votre vision. Faites confiance à Kaymay
            Services pour réaliser vos projets de construction et de rénovation avec expertise et professionnalisme,
            tout en apportant une touche de design unique à chaque réalisation."
"""

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_admin = db.Column(db.Boolean, default=False)
    last_login = db.Column(db.DateTime)

    def __repr__(self):
        return f"User('{self.email}', '{self.name}')"
    

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titre = db.Column(db.String(100))
    soustitre = db.Column(db.String(100))
    contenu = db.Column(db.Text)
    auteur = db.Column(db.String(50))
    date_posted = db.Column(db.DateTime)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    category = db.Column(db.String(50))  # La nouvelle colonne

# models.py
class SiteConfig(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # Informations de base
    company_name = db.Column(db.String(100), default='Kaymay Services')
    email = db.Column(db.String(100), default='info@kaymayservices.com')
    phone = db.Column(db.String(20), default='+243 81 88 48 797')
    address = db.Column(db.Text, default='lubilanshi 407')
    about_content = db.Column(db.Text, default=about_text)
    
    # Images (noms fixes)
    accueil_image = db.Column(db.String(100), default='accueil.jpg')
    about_image = db.Column(db.String(100), default='about.jpg')
    contact_image = db.Column(db.String(100), default='contact.jpg')
    portfolio_1_image = db.Column(db.String(100), default='portfolio1.jpg')
    portfolio_2_image = db.Column(db.String(100), default='portfolio2.jpg')
    portfolio_3_image = db.Column(db.String(100), default='portfolio3.jpg')
    portfolio_4_image = db.Column(db.String(100), default='portfolio4.jpg')
    
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)