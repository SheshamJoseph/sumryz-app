from curses import flash
from flask import render_template, session, redirect, url_for

# from app.auth import views
from . import main
# from ..models import Permissions, User, 
from .. import db
from flask_login import login_required, current_user

@main.route('/', methods=['GET', 'POST'])
def home():

    return render_template('index.html')
