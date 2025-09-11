from flask import Flask
from .config import DB_PARAMS, SECRET_KEY
import os

from dotenv import load_dotenv
load_dotenv()


from flask_mail import Mail
mail = Mail()

def create_app():
    app = Flask(__name__)
    app.secret_key = SECRET_KEY

    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = 'kiwis.cle@gmail.com'
    app.config['MAIL_PASSWORD'] =  os.environ.get('MAIL_SECRET')
    app.config['MAIL_DEFAULT_SENDER'] = 'kiwis.cle@gmail.com'
    mail.init_app(app)

    from .routes import main
    app.register_blueprint(main)
    
    return app