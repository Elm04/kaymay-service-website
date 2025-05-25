from flask import Flask 
from flask_mailman import Mail

mail = Mail()

app = Flask(__name__)
app.config['MAIL_SERVER']="smtp-mail.outlook.com"
app.config['MAIL_PORT']=587
app.config['MAIL_USERNAME']="kaymaydrc@outlook.com"
app.config['MAIL_PASSWORD']="Kay@2024m"
app.config['MAIL_USE_TLS']=True
app.config['MAIL_USE_SSL']=False
mail.init_app(app)

from webapp.views import views

app.register_blueprint(views, url_prefix='/')
app.secret_key = 'mysecretkey'