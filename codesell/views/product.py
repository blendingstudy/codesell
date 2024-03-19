from flask import Blueprint, render_template
from codesell.models import Product

def product_list():
    products = Product.query.all()
    print(products)
    return render_template('product_list.html', products=products)

def product_detail(product_id):
    product = Product.query.get_or_404(product_id)
    return render_template('product_detail.html', product=product)