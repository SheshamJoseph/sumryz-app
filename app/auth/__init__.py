from flask import Blueprint

auth = Blueprint('auth', __name__)

from . import views     # actual fix to routes not being registered
