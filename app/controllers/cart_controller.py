from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models.cart import Cart, CartItem
from app.models.product import Product
from app import db

cart_bp = Blueprint('cart', __name__, url_prefix='/cart')

@cart_bp.route('/')
@login_required
def cart_detail():
    cart = Cart.query.filter_by(user_id=current_user.id).first()
    if not cart:
        cart = Cart(user_id=current_user.id)
        db.session.add(cart)
        db.session.commit()
    cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
    total_price = cart.get_total_price()
    return render_template('cart.html', cart_items=cart_items, total_price=total_price)

@cart_bp.route('/add/<int:product_id>', methods=['POST'])
@login_required
def add_to_cart(product_id):
    quantity = int(request.form.get('quantity', 1))
    product = Product.query.get_or_404(product_id)
    cart = Cart.query.filter_by(user_id=current_user.id).first()
    if not cart:
        cart = Cart(user_id=current_user.id)
        db.session.add(cart)
        db.session.commit()
    cart.add_item(product_id, quantity, cart_id=cart.id)
    flash(f'{product.name} added to cart.', 'success')
    return redirect(url_for('cart.cart_detail'))

@cart_bp.route('/remove/<int:cart_item_id>', methods=['POST'])
@login_required
def remove_from_cart(cart_item_id):
    cart_item = CartItem.query.get_or_404(cart_item_id)
    if cart_item.user_id == current_user.id:
        db.session.delete(cart_item)
        db.session.commit()
        flash('Item removed from cart.', 'success')
    return redirect(url_for('cart.cart_detail'))

@cart_bp.route('/clear', methods=['POST'])
@login_required
def clear_cart():
    cart = Cart.query.filter_by(user_id=current_user.id).first()
    if cart:
        cart.clear()
        flash('Cart cleared.', 'success')
    return redirect(url_for('cart.cart_detail'))