from .. import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    def set_password(self, password):
        """Hash the password for storage."""
        self.password = generate_password_hash(password)
        
    def check_password(self, password):
        """Check the hashed password against the provided password."""
        return check_password_hash(self.password, password)
    
    def __repr__(self):
        return f'<User {self.username}>'

# the table that stores the documents user's have summarized
class Documents(db.Model):
    __tablename__ = 'documents'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    file_path = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(), nullable=False)
    
    user = db.relationship('User', backref=db.backref('documents', lazy=True))
