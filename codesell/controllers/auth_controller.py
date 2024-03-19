from flask import Blueprint
from codesell.views.auth import login, register, logout

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

auth_bp.route('/login', methods=['GET', 'POST'])(login)
auth_bp.route('/register', methods=['GET', 'POST'])(register)
auth_bp.route('/logout')(logout)