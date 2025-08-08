from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, EmailField, PasswordField, BooleanField, ValidationError, TextAreaField
from wtforms.validators import DataRequired, Length, EqualTo, Email

class RegistrationForm(FlaskForm):
    fname = StringField('First Name : ', validators=[DataRequired()])
    lname = StringField('Last name : ', validators=[DataRequired()])
    email = EmailField('Email : ', validators=[DataRequired(), Email()])
    password = PasswordField('Password : ', validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField('Confirm password : ', validators=[DataRequired(), EqualTo('password')])
    # accept = BooleanField('Accept ', validators=[DataRequired()])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    email = EmailField('Email : ', validators=[DataRequired(), Email()])
    password = PasswordField('Password : ', validators=[DataRequired(), Length(min=8)])
    remember = BooleanField('Remember me.')
    submit = SubmitField('Login')
