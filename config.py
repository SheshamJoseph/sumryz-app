from datetime import timedelta
import os
from dotenv import load_dotenv
    
# load environment variables from .env file
load_dotenv()

basedir = os.path.abspath(os.path.dirname(__file__)) # Get the directory of the current file

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    UPLOAD_FOLDER = os.path.join(basedir, 'instance', 'uploads')
    SUMMARY_FOLDER = os.path.join(basedir, 'instance', 'summaries')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'docx', 'doc'}
    REMEMBER_COOKIE_DURATION = timedelta(days=7)  # 7 days

    @staticmethod
    def init_app(app):
        os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
        os.makedirs(Config.SUMMARY_FOLDER, exist_ok=True)
    
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
