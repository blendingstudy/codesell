from flask import Blueprint
from codesell.views.cart import add_to_cart, remove_from_cart, view_cart, checkout

cart_bp = Blueprint('cart', __name__, url_prefix='/cart')

cart_bp.route('/add/<int:product_id>', methods=['POST'])(add_to_cart)
cart_bp.route('/remove/<int:product_id>', methods=['POST'])(remove_from_cart)
cart_bp.route('/', methods=['GET'])(view_cart)
cart_bp.route('/checkout', methods=['POST'])(checkout)