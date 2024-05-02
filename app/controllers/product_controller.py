import os
from flask import Blueprint, current_app, render_template, request, redirect, send_file, url_for, flash
from flask_login import current_user, login_required
from app.models.order import Order
from app.models.product import Product
from app.models.category import Category
from app import db
from app.forms import ProductForm

product_bp = Blueprint('product', __name__, url_prefix='/products')

@product_bp.route('/')
def index():
    language_id = request.args.get('language')
    usage_id = request.args.get('usage')
    
    products = Product.query.filter_by(is_active=True)
    
    if language_id:
        products = products.filter_by(language_id=language_id)
    
    if usage_id:
        products = products.filter_by(category_id=usage_id)
    
    products = products.all()
    
    languages = Category.query.filter_by(type='language').all()
    usages = Category.query.filter_by(type='usage').all()
    
    return render_template('product_list.html', products=products, languages=languages, usages=usages,
                           selected_language=language_id, selected_usage=usage_id)

@product_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_product():
    form = ProductForm()
    language_categories = Category.query.filter_by(type='language').all()
    usage_categories = Category.query.filter_by(type='usage').all()
    
    form.language.choices = [(category.id, category.name) for category in language_categories]
    form.usage.choices = [(category.id, category.name) for category in usage_categories]
    
    if form.validate_on_submit():
        language_id = request.form['language']
        usage_id = request.form['usage']
        code_file = request.files['code_file']

        if code_file:
            filename = code_file.filename
            code_file_path = os.path.join(current_app.root_path, '..', 'uploads', filename)
            code_file.save(code_file_path)
        
        product = Product(
            name=form.name.data,
            description=form.description.data,
            price=form.price.data,
            code_file=code_file_path,
            category_id=usage_id,
            language_id=language_id,
            seller_id=current_user.id
        )
        
        db.session.add(product)
        db.session.commit()
        
        flash('Product created successfully.', 'success')
        return redirect(url_for('product.index'))
    
    return render_template('product_create.html', form=form, language_categories=language_categories, usage_categories=usage_categories)

@product_bp.route('/<int:product_id>')
def get_product(product_id):
    product = Product.query.filter_by(id=product_id, is_active=True).first_or_404()
    return render_template('product_detail.html', product=product)

@product_bp.route('/<int:product_id>/update', methods=['GET', 'POST'])
@login_required
def update_product(product_id):
    product = Product.query.filter_by(id=product_id, is_active=True).first_or_404()
    
    if product.seller_id != current_user.id:
        flash('You are not authorized to update this product.', 'warning')
        return redirect(url_for('product.get_product', product_id=product.id))
    
    language_categories = Category.query.filter_by(type='language').all()
    usage_categories = Category.query.filter_by(type='usage').all()
    
    if request.method == 'POST':
        product.name = request.form['name']
        product.description = request.form['description']
        product.price = request.form['price']
        code_file = request.files['code_file']
        
        if code_file:
            filename = code_file.filename
            code_file_path = os.path.join(current_app.root_path, '..', 'uploads', filename)
            code_file.save(code_file_path)
            product.code_file = code_file_path
        
        product.category_id = request.form['usage']
        
        db.session.commit()
        
        flash('Product updated successfully.', 'success')
        return redirect(url_for('product.get_product', product_id=product.id))
    
    return render_template('product_update.html', product=product, language_categories=language_categories, usage_categories=usage_categories)

@product_bp.route('/<int:product_id>/delete', methods=['POST'])
@login_required
def delete_product(product_id):
    product = Product.query.filter_by(id=product_id, is_active=True).first_or_404()
    
    if product.seller_id != current_user.id:
        flash('You are not authorized to delete this product.', 'warning')
        return redirect(url_for('product.get_product', product_id=product.id))
    
    product.is_active = False
    db.session.commit()
    
    flash('Product deleted successfully.', 'success')
    return redirect(url_for('product.index'))

@product_bp.route('/<int:product_id>/download')
@login_required
def download_code(product_id):
    product = Product.query.filter_by(id=product_id, is_active=True).first_or_404()
    
    if not Order.has_purchased(current_user.id, product):
        flash('You have not purchased this product.', 'warning')
        return redirect(url_for('product.get_product', product_id=product.id))
    
    try:
        code_file_path = os.path.join(current_app.root_path, '..', product.code_file)
        return send_file(code_file_path, as_attachment=True)
    except FileNotFoundError:
        flash('Code file not found.', 'error')
        return redirect(url_for('product.get_product', product_id=product.id))