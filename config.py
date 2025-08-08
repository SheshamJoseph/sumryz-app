import os

basedir = os.path.abspath(os.path.dirname(__file__)) # Get the directory of the current file

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'sghcjnjdscnjknducjnnuebfcncnjdncn'
    UPLOAD_FOLDER = os.path.join(basedir, 'uploads')
    
    @staticmethod
    def init_app(app):
        # Initialize any app-specific configurations here
        pass
    
class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or 'sqlite://'

configs = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
