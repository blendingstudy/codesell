from flask import Blueprint, render_template
from codesell.models import Product

product_bp = Blueprint('product', __name__, url_prefix='/products')

@product_bp.route('/')
def product_list():
    products = Product.query.all()
    print(products)
    return render_template('product_list.html', products=products)

@product_bp.route('/<int:product_id>')
def product_detail(product_id):
    product = Product.query.get_or_404(product_id)
    return render_template('product_detail.html', product=product)