from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from .forms import LoginForm
from . import db, login_manager
from datetime import datetime

auth = Blueprint('auth', __name__)

def create_default_user():
    # Vérifie si l'utilisateur admin existe déjà
    admin_email = "admin@kaymayservices.com"
    existing_admin = User.query.filter_by(email=admin_email).first()
    
    if not existing_admin:
        # Création du compte admin par défaut
        admin_user = User(
            email=admin_email,
            password=generate_password_hash("Admin@Kaymay2024"),  # Mot de passe fort par défaut
            name="Administrateur Kaymay",
            created_at=datetime.utcnow(),
            is_admin=True,
            last_login=None
        )
        
        db.session.add(admin_user)
        db.session.commit()
        print("Compte administrateur par défaut créé avec succès!")

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@auth.route('/kaymay-login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('views.dashboard'))
    
    form = LoginForm()
    
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        
        if user and check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash('Connexion réussie!', 'success')
            return redirect(next_page or url_for('views.dashboard'))
        else:
            flash('Email ou mot de passe incorrect', 'danger')
    
    return render_template('login.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Vous avez été déconnecté avec succès', 'info')
    return redirect(url_for('auth.login'))

@auth.route('/forgot-password')
def forgot_password():
    return render_template('forgot_password.html')