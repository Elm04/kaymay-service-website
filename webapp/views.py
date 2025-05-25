from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_mailman import EmailMessage

views= Blueprint('views',__name__)

@views.route('/')
def index():
    return render_template('index.html')


@views.route('/about')
def about():
    return render_template('about.html')

@views.route('/service')
def service():
    return render_template('service.html')

@views.route('/contact',methods=["GET","POST"])
def contact():
    if request.method=="POST":
        nom = request.form['nom']
        telephone = request.form['telephone']
        email = request.form['email']
        message = request.form['message']

        msg = EmailMessage(
            "Mail qui provient du website",
            f"Nom:{nom}\ttelephone:{telephone}\temail: {email}\n\n{message}",
            "kaymaydrc@outlook.com",
            ["elimuya10@gmail.com"]
        )
        msg.send()
        flash('Merdci de nous avoir contacter, Nous allons vous répondre dans un bref delai', 'success')
        return redirect(url_for('views.contact'))
    return render_template('contact.html')