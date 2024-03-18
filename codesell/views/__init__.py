""" from flask import Blueprint

bp = Blueprint('main', __name__, url_prefix = '/')
auth_bp = Blueprint('auth', __name__, url_prefix = '/auth')

print('views/init')

from . import main
 """