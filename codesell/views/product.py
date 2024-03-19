from flask import Blueprint, render_template
from codesell.controllers.product_controller import product_list

product_bp = Blueprint('product', __name__, url_prefix='/products')

product_bp.add_url_rule('/', view_func=product_list)