# This file initializes the Flask application and sets up the database connection.
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from config import configs


db = SQLAlchemy()
mail = Mail()
login_manager = LoginManager()


def create_app(config_name='default'):
    app = Flask(__name__)
    
    # Load the configuration
    app.config.from_object(configs[config_name])
    
    # configure mail settings
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = 'your_email@gmail.com'
    app.config['MAIL_PASSWORD'] = 'your_email_password'
    app.config['MAIL_DEFAULT_SENDER'] = 'your_email@gmail.com'

    # Initialize the database
    db.init_app(app)
    
    mail.init_app(app)
    
    # Initialize the login manager
    
    # login_manager.login = 'auth.login'
    login_manager.init_app(app)
    
    # Register blueprints or other app components here
    from .auth import auth as auth_blueprint
    
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    
    
    return app
