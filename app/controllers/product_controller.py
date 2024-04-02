from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.product import Product
from app.models.category import Category
from app import db
from app.forms import ProductForm

product_bp = Blueprint('product', __name__, url_prefix='/products')

@product_bp.route('/')
def index():
    products = Product.query.all()
    return render_template('product_list.html', products=products)

@product_bp.route('/create', methods=['GET', 'POST'])
def create_product():
    form = ProductForm()
    categories = Category.query.all()
    form.category_id.choices = [(category.id, category.name) for category in categories]
    if form.validate_on_submit():
        product = Product(
            name=form.name.data,
            description=form.description.data,
            price=form.price.data,
            quantity=form.quantity.data,
            image_url=form.image_url.data,
            category_id=form.category_id.data
        )
        db.session.add(product)
        db.session.commit()
        flash('Product created successfully.', 'success')
        return redirect(url_for('product.index'))
    
    return render_template('product_create.html', form=form)

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

""" @product_bp.route('/create', methods=['GET', 'POST'])
def create_product():
    form = ProductForm()
    if form.validate_on_submit():
        product = Product(
            name=form.name.data,
            description=form.description.data,
            price=form.price.data,
            quantity=form.quantity.data
        )
        db.session.add(product)
        db.session.commit()
        flash('Product created successfully.', 'success')
        return redirect(url_for('product.index'))
    return render_template('product/create.html', form=form) """