from flask import Blueprint

bp = Blueprint('main', __name__, url_prefix = '/')
auth_bp = Blueprint('auth', __name__)
