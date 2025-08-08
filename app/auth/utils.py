import flask_mail
from itsdangerous import URLSafeTimedSerializer
from flask import current_app
from flask_mail import Message
from .. import mail

def generate_reset_token(email):
    s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    return s.dumps(email, salt='password-reset-salt')

def verify_reset_token(token, expiration=3600):
    s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    try:
        email = s.loads(token, salt='password-reset-salt', max_age=expiration)
    except:
        return None
    return email

def send_password_reset_email(user):
    token = generate_reset_token(user.email)
    msg = Message('Password Reset Request',
                  recipients=[user.email])
    # TODO: Define a better template for the email body
    msg.subject = 'Reset Your Password'
    msg.html = f'''<p>To reset your password, visit the following link:</p>
                   <p><a href="{current_app.config['BASE_URL']}/reset_password/{token}">Reset Password</a></p>
                   <p>If you did not make this request then simply ignore this email and no changes will be made.</p>'''
    
    mail.send(msg)
    return True
