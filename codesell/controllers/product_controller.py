from flask import Blueprint, render_template
from codesell.views.product import product_list, product_detail

product_bp = Blueprint('product', __name__, url_prefix='/products')

product_bp.route('/')(product_list)
product_bp.route('/<int:product_id>')(product_detail)