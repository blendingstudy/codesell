from flask import render_template, redirect, url_for, flash, request, Blueprint
from flask_login import login_required, current_user
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
        return redirect(url_for('main.index'))
    products = Product.query.all()
    return render_template('product_list.html', products=products)

@admin_bp.route('/orders')
@login_required
def order_list():
    if not current_user.is_admin:
        flash('Access denied. Admin privileges required.', 'danger')
        return redirect(url_for('main.index'))
    orders = Order.query.all()
    return render_template('order_list.html', orders=orders)