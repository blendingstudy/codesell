from flask import Blueprint

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')
product_bp = Blueprint('product', __name__, url_prefix='/products')
cart_bp = Blueprint('cart', __name__, url_prefix='/cart')
order_bp = Blueprint('order', __name__, url_prefix='/orders')
funding_bp = Blueprint('funding', __name__, url_prefix='/funding')
admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

from app.controllers import auth_controller, product_controller, cart_controller, order_controller, funding_controller, admin_controller