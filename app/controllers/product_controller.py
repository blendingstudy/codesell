from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.product import Product
from app.models.category import Category
from app import db
from app.forms import ProductForm

product_bp = Blueprint('product', __name__, url_prefix='/products')

@product_bp.route('/')
def index():
    language_id = request.args.get('language')
    usage_id = request.args.get('usage')
    
    products = Product.query
    
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
def create_product():
    form = ProductForm()
    language_categories = Category.query.filter_by(type='language').all()
    usage_categories = Category.query.filter_by(type='usage').all()
    
    form.language.choices = [(category.id, category.name) for category in language_categories]
    form.usage.choices = [(category.id, category.name) for category in usage_categories]
    
    if form.validate_on_submit():
        language_id = request.form['language']
        usage_id = request.form['usage']
        
        product = Product(
            name=form.name.data,
            description=form.description.data,
            price=form.price.data,
            quantity=form.quantity.data,
            image_url=form.image_url.data,
            category_id=usage_id,
            language_id=language_id
        )
        
        db.session.add(product)
        db.session.commit()
        
        flash('Product created successfully.', 'success')
        return redirect(url_for('product.index'))
    
    return render_template('product_create.html', form=form, language_categories=language_categories, usage_categories=usage_categories)

@product_bp.route('/<int:product_id>')
def get_product(product_id):
    product = Product.query.get_or_404(product_id)
    return render_template('product_detail.html', product=product)

@product_bp.route('/<int:product_id>/update', methods=['GET', 'POST'])
def update_product(product_id):
    product = Product.query.get_or_404(product_id)
    
    language_categories = Category.query.filter_by(type='language').all()
    usage_categories = Category.query.filter_by(type='usage').all()
    
    if request.method == 'POST':
        product.name = request.form['name']
        product.description = request.form['description']
        product.price = request.form['price']
        product.quantity = request.form['quantity']
        product.image_url = request.form['image_url']
        product.category_id = request.form['usage']
        
        db.session.commit()
        
        flash('Product updated successfully.', 'success')
        return redirect(url_for('product.get_product', product_id=product.id))
    
    return render_template('product_update.html', product=product, language_categories=language_categories, usage_categories=usage_categories)

@product_bp.route('/<int:product_id>/delete', methods=['POST'])
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    
    flash('Product deleted successfully.', 'success')
    return redirect(url_for('product.index'))