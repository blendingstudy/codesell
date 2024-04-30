from flask import render_template, redirect, url_for, flash, request, Blueprint
from flask_login import login_required, current_user
from app.models.category import Category
from app.models.user import User
from app.models.product import Product
from app.models.order import Order
from app import db

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/')
@login_required
def index():
    if not current_user.is_admin:
        flash('Access denied. Admin privileges required.', 'danger')
        return redirect(url_for('main.index'))
    return render_template('admin_index.html')

@admin_bp.route('/users')
@login_required
def user_list():
    if not current_user.is_admin:
        flash('Access denied. Admin privileges required.', 'danger')
        return redirect(url_for('main.index'))
    users = User.query.all()
    return render_template('user_list.html', users=users)

@admin_bp.route('/products')
@login_required
def product_list():
    if not current_user.is_admin:
        flash('Access denied. Admin privileges required.', 'danger')
        return redirect(url_for('index'))
    products = Product.query.filter_by(is_active=True)
    return render_template('admin_product_list.html', products=products)

@admin_bp.route('/orders')
@login_required
def order_list():
    if not current_user.is_admin:
        flash('Access denied. Admin privileges required.', 'danger')
        return redirect(url_for('index'))
    orders = Order.query.all()
    return render_template('order_list.html', orders=orders)

@admin_bp.route('/users/<int:user_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_user(user_id):
    if not current_user.is_admin:
        flash('Access denied. Admin privileges required.', 'danger')
        return redirect(url_for('index'))
    user = User.query.get_or_404(user_id)
    if request.method == 'POST':
        user.username = request.form['username']
        user.email = request.form['email']
        user.is_admin = 'is_admin' in request.form
        db.session.commit()
        flash('User updated successfully.', 'success')
        return redirect(url_for('admin.user_list'))
    return render_template('edit_user.html', user=user)

@admin_bp.route('/users/<int:user_id>/delete', methods=['POST'])
@login_required
def delete_user(user_id):
    if not current_user.is_admin:
        flash('Access denied. Admin privileges required.', 'danger')
        return redirect(url_for('index'))
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash('User deleted successfully.', 'success')
    return redirect(url_for('admin.user_list')) 

@admin_bp.route('/products/<int:product_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_product(product_id):
    if not current_user.is_admin:
        flash('Access denied. Admin privileges required.', 'danger')
        return redirect(url_for('index'))
    product = Product.query.get_or_404(product_id)
    language_categories = Category.query.filter_by(type='language').all()
    usage_categories = Category.query.filter_by(type='usage').all()
    users = User.query.all()
    
    if request.method == 'POST':
        product.name = request.form['name']
        product.description = request.form['description']
        product.price = request.form['price']
        product.quantity = request.form['quantity']
        product.image_url = request.form['image_url']
        product.category_id = request.form['category_id']
        product.language_id = request.form['language_id']
        product.seller_id = request.form['seller_id']
        db.session.commit()
        flash('Product updated successfully.', 'success')
        return redirect(url_for('admin.product_list'))
    return render_template('edit_product.html', product=product, language_categories=language_categories, usage_categories=usage_categories, users=users)

@admin_bp.route('/products/<int:product_id>/delete', methods=['POST'])
@login_required
def delete_product(product_id):
   if not current_user.is_admin:
       flash('Access denied. Admin privileges required.', 'danger')
       return redirect(url_for('index'))
   product = Product.query.get_or_404(product_id)
   product.is_active = False
   db.session.commit()
   flash('Product deleted successfully.', 'success')
   return redirect(url_for('admin.product_list'))
