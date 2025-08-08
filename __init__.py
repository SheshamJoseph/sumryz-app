# This file initializes the Flask application and sets up the database connection.
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import configs

db = SQLAlchemy()

def create_app(config_name='default'):
    app = Flask(__name__)
    
    # Load the configuration
    app.config.from_object(configs[config_name])
    
    # Initialize the database
    db.init_app(app)
    
    # Initialize the login manager
    
    login_manager = LoginManager()
    # login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    
    # Register blueprints or other app components here
    
    return app
