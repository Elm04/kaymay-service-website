from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_mailman import EmailMessage
from webapp.forms import PostForm, SiteConfigForm, ContactForm
from webapp.models import Post, SiteConfig
from flask_login import current_user,login_required
from . import db
from werkzeug.utils import secure_filename
from PIL import Image
import os
from datetime import datetime
from flask import current_app, request

views= Blueprint('views',__name__)

@views.route('/')
def index():
    config = SiteConfig.query.first()
    print(config.email)
    return render_template('index.html', config=config)

@views.route('/new-blog')
def new_blog():
    form = PostForm()
    return render_template('new_blog.html', form=form)

@views.route('/dashboard')
@login_required  # Assurez-vous que seul l'admin peut accéder
def dashboard():
    try:
        # Récupération du numéro de page (par défaut 1)
        page = request.args.get('page', 1, type=int)
        
        # Nombre d'articles par page
        per_page = 10
        
        # Récupération des posts avec pagination et tri par date décroissante
        posts = Post.query.order_by(
            Post.date_posted.desc()
        ).paginate(
            page=page, 
            per_page=per_page, 
            error_out=False
        )
        
        # Statistiques pour le dashboard
        stats = {
            'total_posts': Post.query.count(),
            'posts_this_month': Post.query.filter(
                Post.date_posted >= datetime.utcnow().replace(day=1, hour=0, minute=0, second=0)
            ).count(),
            # Suppression de la stat sur les drafts si le champ n'existe pas
            'recent_posts': Post.query.order_by(
                Post.date_posted.desc()
            ).limit(5).all()
        }
        print(f"verification statut:{stats}\nVerification Post{posts}")
        return render_template(
            'dashboard.html',
            posts=posts,
            stats=stats,
            now=datetime.utcnow()
        )
        
    except Exception as e:
        current_app.logger.error(f"Erreur dashboard: {str(e)}")
        flash("Une erreur est survenue lors du chargement du tableau de bord.", "danger")
        print(f"Nous avons une erreur:\n{e}")
        return redirect(url_for('views.new_blog'))



@views.route('/kaymay-service/réalisation')
def realisations():
    return render_template('realisations.html')


@views.route('/about')
def about():
    return render_template('about.html')

@views.route('/service')
def service():
    return render_template('service.html')

@views.route('/details/<int:id_post>')
def detail(id_post):
	post=Post.query.filter_by(id=id_post).first()

	return render_template('detailpost.html', post=post)


@views.route('/add-blog', methods=["GET", "POST"])
@login_required  # Décommentez quand vous aurez implémenté l'authentification
def addblog():
    form = PostForm()
    
    if form.validate_on_submit():
        try:
            # Gestion de l'image
            image = form.image.data
            if image:
                # Sécurisation du nom de fichier
                original_filename = secure_filename(image.filename)
                unique_filename = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{os.urandom(4).hex()}.{original_filename.split('.')[-1].lower()}"
                
                # Chemins de stockage
                upload_folder = os.path.join(current_app.root_path, 'static', 'uploads', 'blog')
                os.makedirs(upload_folder, exist_ok=True)
                
                # Sauvegarde de l'image originale
                image_path = os.path.join(upload_folder, unique_filename)
                image.save(image_path)
                
                # Création des versions redimensionnées
                sizes = {
                    'thumbnail': (400, 400),
                    'medium': (800, 800),
                    'large': (1200, 1200)
                }
                
                for size_name, dimensions in sizes.items():
                    output_folder = os.path.join(upload_folder, size_name)
                    os.makedirs(output_folder, exist_ok=True)
                    
                    img = Image.open(image_path)
                    img.thumbnail(dimensions)
                    img.save(os.path.join(output_folder, f"{size_name}_{unique_filename}"), quality=85)
            
            # Création du post
            post = Post(
                titre=form.titre.data,
                soustitre=form.soustitre.data,
                auteur=current_user.name if current_user.is_authenticated else form.auteur.data,
                contenu=form.contenu.data,
                date_posted=datetime.utcnow(),
                image_file=unique_filename if image else None,
                # slug=generate_slug(form.titre.data)  # À implémenter
            )
            
            db.session.add(post)
            db.session.commit()
            
            flash('Article publié avec succès!', 'success')
            return redirect(url_for('views.dashboard'))
            
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Erreur lors de la création de l'article: {str(e)}")
            flash("Une erreur est survenue lors de la publication. Veuillez réessayer.", 'danger')
            print(f'Il y a une erreur:\n{e}')
    
    return render_template("new_blog.html", form=form)

@views.route('/contact', methods=["GET", "POST"])
def contact():
    form = ContactForm()
    
    if form.validate_on_submit():
        try:
            msg = EmailMessage(
                subject=f"Nouveau contact depuis le site - {form.nom.data}",
                body=f"""
                Nom: {form.nom.data}
                Téléphone: {form.telephone.data}
                Email: {form.email.data}
                
                Message:
                {form.message.data}
                """,
                from_email="kaymaydrc@outlook.com",
                to=["elimuya10@gmail.com"],
                reply_to=[form.email.data]
            )
            msg.send()
            
            flash('Merci pour votre message. Nous vous répondrons dans les plus brefs délais.', 'success')
            return redirect(url_for('views.contact'))
            
        except Exception as e:
            current_app.logger.error(f"Erreur envoi email: {str(e)}")
            flash(f"Une erreur s'est produite lors de l'envoi du message. Veuillez réessayer. {e}", 'danger')
    
    return render_template('contact.html', form=form)


@views.route('/kaymay-blog')
def blog():
    page = request.args.get('page', 1, type=int)
    search_query = request.args.get('q', '')
    category = request.args.get('category', None)
    
    # Base query
    posts_query = Post.query.order_by(Post.date_posted.desc())
    
    # Apply filters
    if search_query:
        posts_query = posts_query.filter(Post.titre.ilike(f'%{search_query}%') | 
                      posts_query.filter(Post.contenu.ilike(f'%{search_query}%')))
    
    if category:
        posts_query = posts_query.filter_by(category=category)
    
    # Get categories for filter
    categories = [c[0] for c in db.session.query(Post.category).distinct() if c[0]]
    
    # Pagination
    posts = posts_query.paginate(page=page, per_page=6)
    
    # Featured post (most recent)
    featured_post = Post.query.order_by(Post.date_posted.desc()).first()
    
    return render_template('blog.html',
                         posts=posts,
                         featured_post=featured_post,
                         categories=categories,
                         active_category=category)


@views.route('/update/<int:id_post>/modifier', methods=['GET', 'POST'])
@login_required
def update_post(id_post):
    post = Post.query.get_or_404(id_post)
    form = PostForm(obj=post)  # Pré-remplir le formulaire avec les données existantes

    if form.validate_on_submit():
        try:
            # Gestion de l'image
            if form.image.data:  # Si nouvelle image fournie
                # Supprimer les anciennes images si elles existent
                for filename in [post.image_file, 'resized_' + post.image_file]:
                    if filename:
                        old_path = os.path.join(current_app.root_path, 'static', 'uploads', 'blog', filename)
                        if os.path.exists(old_path):
                            os.remove(old_path)

                # Sauvegarder la nouvelle image
                image = form.image.data
                filename = secure_filename(image.filename)
                unique_filename = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{os.urandom(4).hex()}.{filename.split('.')[-1].lower()}"
                
                upload_path = os.path.join(current_app.root_path, 'static', 'uploads', 'blog')
                os.makedirs(upload_path, exist_ok=True)
                
                image_path = os.path.join(upload_path, unique_filename)
                image.save(image_path)
                
                # Créer une version redimensionnée
                img = Image.open(image_path)
                img.thumbnail((800, 800))  # Conserver le ratio d'aspect
                img.save(os.path.join(upload_path, 'resized_' + unique_filename), quality=85)
                
                post.image_file = unique_filename

            # Mettre à jour les autres champs
            post.titre = form.titre.data
            post.soustitre = form.soustitre.data
            post.auteur = form.auteur.data
            post.contenu = form.contenu.data
            post.category = form.category.data if hasattr(form, 'category') else None
            post.date_updated = datetime.utcnow()  # Ajouter un champ de mise à jour

            db.session.commit()
            flash('L\'article a été modifié avec succès!', 'success')
            return redirect(url_for('views.dashboard'))

        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Erreur modification article: {str(e)}")
            flash("Une erreur est survenue lors de la modification", 'danger')

    # Pour GET ou si form.validate_on_submit() échoue
    return render_template('edit_post.html', form=form, post=post)

@views.route('/delete/<int:id_post>/delete', methods=['GET', 'POST'])
@login_required  # Protection de la route
def delete_post(id_post):
    post = Post.query.get_or_404(id_post)
    
    try:
        # Chemin vers le dossier des uploads
        upload_dir = os.path.join(current_app.root_path, 'static', 'uploads', 'blog')
        
        # Suppression des fichiers image
        if post.image_file:
            # Supprime l'image originale
            original_path = os.path.join(upload_dir, post.image_file)
            if os.path.exists(original_path):
                os.remove(original_path)
            
            # Supprime l'image redimensionnée si elle existe
            resized_path = os.path.join(upload_dir, 'resized_' + post.image_file)
            if os.path.exists(resized_path):
                os.remove(resized_path)
        
        # Suppression de la base de données
        db.session.delete(post)
        db.session.commit()
        
        flash('L\'article a été supprimé avec succès', 'success')
        current_app.logger.info(f"Article {id_post} supprimé avec succès")
    
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Erreur suppression article {id_post}: {str(e)}")
        flash('Une erreur est survenue lors de la suppression', 'danger')
    
    return redirect(url_for('views.dashboard'))


@views.route('/kaymay-config', methods=['GET', 'POST'])
@login_required
def configuration():
    config = SiteConfig.query.first() or SiteConfig()
    if not config.id:
        db.session.add(config)
        db.session.commit()
    
    form = SiteConfigForm(obj=config)
    
    if form.validate_on_submit():
        try:
            upload_dir = os.path.join(current_app.root_path, 'static', 'uploads', 'config')
            os.makedirs(upload_dir, exist_ok=True)
            
            # Gestion des images avec noms fixes
            for field_name in SiteConfigForm.image_fields:
                field = getattr(form, field_name)
                if field.data:
                    filename = f"{field_name}.{secure_filename(field.data.filename).split('.')[-1]}"
                    filepath = os.path.join(upload_dir, filename)
                    
                    # Supprimer l'ancienne si elle existe
                    if os.path.exists(filepath):
                        os.remove(filepath)
                    
                    # Sauvegarder la nouvelle
                    field.data.save(filepath)
                    setattr(config, field_name, filename)
            
            # Mise à jour des autres champs
            form.populate_obj(config)
            db.session.commit()
            
            flash('Configuration enregistrée avec succès!', 'success')
            return redirect(url_for('views.configuration'))
            
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Erreur configuration: {str(e)}")
            flash('Erreur lors de la mise à jour', 'danger')
    
    return render_template('parametre.html', form=form, config=config)