import os
from flask import Blueprint, current_app, render_template, request, redirect, send_file, url_for, flash
from flask_login import current_user, login_required
from app.models.order import Order
from app.models.product import Product
from app.models.category import Category
from app import db
from app.forms import ProductForm, SearchForm

product_bp = Blueprint('product', __name__, url_prefix='/products')

@product_bp.route('/', methods=['GET', 'POST'])
def index():
    search_form = SearchForm()
    language_categories = Category.query.filter_by(type='language').all()
    usage_categories = Category.query.filter_by(type='usage').all()

    search_form.language.choices = [(0, 'All Languages')] + [(category.id, category.name) for category in language_categories]
    search_form.usage.choices = [(0, 'All Usages')] + [(category.id, category.name) for category in usage_categories]

    products = Product.query.filter_by(is_active=True)

    if search_form.validate_on_submit():
        keyword = search_form.keyword.data
        min_price = search_form.min_price.data
        max_price = search_form.max_price.data
        language_id = search_form.language.data
        usage_id = search_form.usage.data

        if keyword:
            products = products.filter(Product.name.ilike(f'%{keyword}%'))
        if min_price:
            products = products.filter(Product.price >= min_price)
        if max_price:
            products = products.filter(Product.price <= max_price)
        if language_id:
            products = products.filter_by(language_id=language_id)
        if usage_id:
            products = products.filter_by(category_id=usage_id)

    products = products.all()

    return render_template('product_list.html', products=products, search_form=search_form)

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
    
""" @product_bp.route('/search')
def search():
    search_form = SearchForm()
    language_categories = Category.query.filter_by(type='language').all()
    usage_categories = Category.query.filter_by(type='usage').all()

    search_form.language.choices = [(0, 'All Languages')] + [(category.id, category.name) for category in language_categories]
    search_form.usage.choices = [(0, 'All Usages')] + [(category.id, category.name) for category in usage_categories]

    keyword = request.args.get('keyword')
    min_price = request.args.get('min_price')
    max_price = request.args.get('max_price')
    language_id = request.args.get('language')
    usage_id = request.args.get('usage')

    products = Product.query.filter_by(is_active=True)

    conditions = []

    if keyword:
        conditions.append(Product.name.ilike(f'%{keyword}%'))

    category_conditions = []
    if language_id and usage_id:
        category_conditions.append(db.and_(Product.language_id == language_id, Product.category_id == usage_id))
    elif language_id:
        category_conditions.append(db.or_(Product.language_id == language_id))
    elif usage_id:
        category_conditions.append(db.or_(Product.category_id == usage_id))
    conditions.append(db.and_(*category_conditions))

    if min_price or max_price:
        price_conditions = []
        if min_price:
            price_conditions.append(db.and_(Product.price >= min_price))
        if max_price:
            price_conditions.append(db.and_(Product.price <= max_price))
        conditions.append(db.and_(*price_conditions))

    if conditions:
        products = products.filter(db.or_(*conditions))

    print(conditions)
    products = products.all()

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return render_template('search_results_partial.html', products=products)

    return render_template('search_results.html', products=products, search_form=search_form) """

@product_bp.route('/search')
def search():
    search_form = SearchForm()
    language_categories = Category.query.filter_by(type='language').all()
    usage_categories = Category.query.filter_by(type='usage').all()

    search_form.language.choices = [(0, 'All Languages')] + [(category.id, category.name) for category in language_categories]
    search_form.usage.choices = [(0, 'All Usages')] + [(category.id, category.name) for category in usage_categories]

    keyword = request.args.get('keyword')
    min_price = request.args.get('min_price')
    max_price = request.args.get('max_price')
    language_id = request.args.get('language')
    usage_id = request.args.get('usage')

    products = Product.query.filter_by(is_active=True)

    if keyword:
        products = products.filter(Product.name.ilike(f'%{keyword}%'))
        print(keyword)
    if min_price:
        products = products.filter(Product.price >= min_price)
        print(min_price)
    if max_price:
        products = products.filter(Product.price <= max_price)
        print(max_price)
    if language_id != '0':
        products = products.filter_by(language_id=language_id)
        print(language_id)
    if usage_id != '0':
        products = products.filter_by(category_id=usage_id)
        print(usage_id)

    products = products.all()

    return render_template('search_results.html', products=products, search_form=search_form)