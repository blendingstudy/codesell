from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.product import Product
from app import db

product_bp = Blueprint('product', __name__, url_prefix='/products')

@product_bp.route('/')
def index():
    products = Product.query.all()
    return render_template('product_list.html', products=products)

@product_bp.route('/create', methods=['GET', 'POST'])
def create_product():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        price = request.form['price']
        quantity = request.form['quantity']
        image_url = request.form['image_url']
        category_id = request.form['category_id']

        new_product = Product(name, description, price, quantity, image_url, category_id)
        db.session.add(new_product)
        db.session.commit()

        flash('Product created successfully.', 'success')
        return redirect(url_for('products'))

    return render_template('product/create.html') #필요

@product_bp.route('/<int:product_id>')
def get_product(product_id):
    product = Product.query.get_or_404(product_id)
    return render_template('product_detail.html', product=product)

@product_bp.route('/<int:product_id>/update', methods=['GET', 'POST'])
def update_product(product_id):
    product = Product.query.get_or_404(product_id)

    if request.method == 'POST':
        product.name = request.form['name']
        product.description = request.form['description']
        product.price = request.form['price']
        product.quantity = request.form['quantity']
        product.image_url = request.form['image_url']
        product.category_id = request.form['category_id']

        db.session.commit()

        flash('Product updated successfully.', 'success')
        return redirect(url_for('product.get_product', product_id=product.id))

    return render_template('product/update.html', product=product)

@product_bp.route('/<int:product_id>/delete', methods=['POST'])
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()

    flash('Product deleted successfully.', 'success')
    return redirect(url_for('products'))