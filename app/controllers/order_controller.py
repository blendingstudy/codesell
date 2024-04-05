from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models.order import Order, OrderItem
from app.models.cart import Cart, CartItem
from app import db

order_bp = Blueprint('order', __name__, url_prefix='/orders')

@order_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_order():
    cart = Cart.query.filter_by(user_id=current_user.id).first()
    if not cart or not cart.items:
        flash('Your cart is empty. Please add items to the cart before creating an order.', 'error')
        return redirect(url_for('cart.cart_detail'))

    if request.method == 'POST':
        shipping_address = request.form['shipping_address']
        order = Order(user_id=current_user.id, total_amount=cart.get_total_price(), shipping_address=shipping_address)
        db.session.add(order)
        db.session.commit()

        for cart_item in cart.items:
            order_item = OrderItem(order_id=order.id, product_id=cart_item.product_id, quantity=cart_item.quantity, price=cart_item.product.price)
            db.session.add(order_item)
        db.session.commit()

        cart.clear()
        flash('Order created successfully.', 'success')
        return redirect(url_for('order.order_detail', order_id=order.id))

    return render_template('checkout.html', cart=cart)

@order_bp.route('/<int:order_id>')
@login_required
def order_detail(order_id):
    order = Order.query.get_or_404(order_id)
    if order.user_id != current_user.id:
        flash('You do not have permission to view this order.', 'error')
        return redirect(url_for('main.index'))
    return render_template('order_detail.html', order=order)

@order_bp.route('/')
@login_required
def order_list():
    orders = Order.query.filter_by(user_id=current_user.id).all()
    return render_template('order_list.html', orders=orders)