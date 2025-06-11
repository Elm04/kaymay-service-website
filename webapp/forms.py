from flask_wtf import FlaskForm

from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, InputRequired 
from wtforms import DateField, SelectField, StringField, IntegerField, FileField, EmailField,SubmitField, PasswordField,BooleanField, TextAreaField,validators

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Mot de passe', validators=[DataRequired(), Length(min=6)])
    remember = BooleanField('Se souvenir de moi')
    submit = SubmitField('Se connecter')

class PostForm(FlaskForm):
	titre = StringField('Titre', validators=[Length(min=5, max=100)])
	soustitre = StringField('Sous Titre')
	auteur = StringField("Auteur")
	contenu = TextAreaField('Contenu')
	date_post = DateField()
	image = FileField('Image du Blog', validators=[DataRequired(), FileAllowed(['jpg','png'], "Seuls les fichiers JPG et PNG peuvent être autorisé!")])
	submit = SubmitField('Poster')
      


class SiteConfigForm(FlaskForm):
    # Champs obligatoires
    company_name = StringField('Nom de l\'entreprise', validators=[InputRequired()])
    email = StringField('Email', validators=[InputRequired(), Email()])
    phone = StringField('Téléphone', validators=[InputRequired()])
    address = TextAreaField('Adresse', validators=[InputRequired()])
    about_content = TextAreaField('Contenu À Propos', validators=[InputRequired()])
    
    # Champs images (optionnels)
    image_fields = {
        'accueil_image': 'Image Accueil',
        'about_image': 'Image À Propos',
        'contact_image': 'Image Contact',
        'portfolio_1_image': 'Portfolio 1',
        'portfolio_2_image': 'Portfolio 2', 
        'portfolio_3_image': 'Portfolio 3',
        'portfolio_4_image': 'Portfolio 4'
    }
    
    for field_name, label in image_fields.items():
        locals()[field_name] = FileField(label, validators=[
            FileAllowed(['jpg', 'jpeg', 'png'], 'Images seulement (JPG, PNG)')
        ])
    
    submit = SubmitField('Enregistrer')

class ContactForm(FlaskForm):
    nom = StringField('Nom', [
        validators.InputRequired(message="Le nom est requis"),
        validators.Length(min=2, max=50)
    ])
    telephone = StringField('Téléphone', [
        validators.InputRequired(),
        validators.Regexp(r'^\+?[\d\s-]{10,15}$', message="Numéro invalide")
    ])
    email = StringField('Email', [
        validators.InputRequired(),
        validators.Email(),
        validators.Length(max=100)
    ])
    message = TextAreaField('Message', [
        validators.InputRequired(),
        validators.Length(min=10, max=2000)
    ])