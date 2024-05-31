from flask import Blueprint, render_template, redirect, request, url_for, flash
from flask_login import login_required, current_user
from app.models.order import Order
from app.models.cart import CartItem
from app import db
from app.models.product import Product
from werkzeug.security import check_password_hash, generate_password_hash

mypage_bp = Blueprint('mypage', __name__, url_prefix='/mypage')

@mypage_bp.route('/')
@login_required
def index():
    orders = Order.query.filter_by(user_id=current_user.id).all()
    cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
    received_gifts = current_user.received_gifts
    return render_template('mypage_index.html', orders=orders, cart_items=cart_items, received_gifts=received_gifts)

@mypage_bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    if request.method == 'POST':
        current_user.username = request.form['username']
        
        current_password = request.form['current_password']
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']
        
        if not check_password_hash(current_user.password_hash, current_password):
            flash('Invalid current password.', 'error')
        elif new_password != confirm_password:
            flash('New passwords do not match.', 'error')
        else:
            current_user.password_hash = generate_password_hash(new_password)
            db.session.commit()
            flash('Profile updated successfully.', 'success')
            return redirect(url_for('mypage.index'))
    
    return render_template('edit_profile.html', user=current_user)

@mypage_bp.route('/my_products')
@login_required
def my_products():
    products = Product.query.filter_by(seller_id=current_user.id).all()
    return render_template('myproducts.html', products=products)

@mypage_bp.route('/manage_product/<int:product_id>', methods=['GET', 'POST'])
@login_required
def manage_product(product_id):
    product = Product.query.get_or_404(product_id)
    if product.seller_id != current_user.id:
        flash('You are not authorized to manage this product.', 'error')
        return redirect(url_for('mypage.my_products'))
    
    if request.method == 'POST':
        product.name = request.form['name']
        product.description = request.form['description']
        product.price = float(request.form['price'])
        
        code_file = request.files.get('code_file')
        if code_file:
            filename = code_file.filename
            code_file_path = os.path.join('uploads', filename)
            code_file.save(code_file_path)
            product.code_file = code_file_path
        
        product.category_id = int(request.form['category_id'])
        db.session.commit()
        
        flash('Product updated successfully.', 'success')
        return redirect(url_for('mypage.my_products'))
    
    return render_template('manage_product.html', product=product)

@mypage_bp.route('/delete_product/<int:product_id>', methods=['POST'])
@login_required
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    if product.seller_id != current_user.id:
        flash('You are not authorized to delete this product.', 'error')
        return redirect(url_for('mypage.my_products'))
    
    db.session.delete(product)
    db.session.commit()
    
    flash('Product deleted successfully.', 'success')
    return redirect(url_for('mypage.my_products'))
