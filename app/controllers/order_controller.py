import json
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from app.models.order import Order, OrderItem
from app.models.cart import Cart, CartItem
from app import db

order_bp = Blueprint('order', __name__, url_prefix='/orders')

@order_bp.route('/checkout', methods=['POST'])
@login_required
def checkout():
    selected_items = request.form.getlist('selected_items')
    if not selected_items:
        flash('No items selected for checkout.', 'warning')
        return redirect(url_for('cart.cart_detail'))

    cart_items = CartItem.query.filter(CartItem.id.in_(selected_items)).all()
    print('cart_items')
    print(cart_items)
    if not cart_items:
        flash('Invalid cart items selected.', 'danger')
        return redirect(url_for('cart.cart_detail'))

    total_amount = sum(item.product.price * item.quantity for item in cart_items)

    return render_template('checkout.html', cart=cart_items, total_amount=total_amount)

@order_bp.route('/create', methods=['POST'])
@login_required
def create_order():
    shipping_address = request.form['shipping_address']
    imp_uid = request.form.get('imp_uid')
    merchant_uid = request.form.get('merchant_uid')

    # 선택된 상품 정보 가져오기
    selected_items_str = request.form.get('selected_items')
    selected_items = json.loads(selected_items_str) if selected_items_str else []
    #selected_items = request.form.getlist('selected_items')
    cart_items = CartItem.query.filter(CartItem.id.in_(selected_items)).all()
    total_amount = request.form.get('total_amount')

    print(selected_items)
    order = Order(user_id=current_user.id, total_amount=total_amount, shipping_address=shipping_address)
    order.status = 'paid'  # 결제 완료 상태로 설정
    db.session.add(order)
    db.session.commit()

    for item in cart_items:
        order_item = OrderItem(order_id=order.id, product_id=item.product_id, quantity=item.quantity, price=item.product.price)
        db.session.add(order_item)
        # 재고 변경 로직 추가

    db.session.commit()

    # 장바구니에서 주문한 아이템 제거
    for item in cart_items:
        db.session.delete(item)
    db.session.commit()

    flash('Order created successfully.', 'success')
    return jsonify({'order_id': order.id})

@order_bp.route('/<int:order_id>')
@login_required
def order_detail(order_id):
    order = Order.query.get_or_404(order_id)
    if order.user_id != current_user.id and current_user.is_admin is False:
        flash('You do not have permission to view this order.', 'error')
        return redirect(url_for('index'))
    return render_template('order_detail.html', order=order)

@order_bp.route('/')
@login_required
def order_list():
    if current_user.is_admin:
        return redirect(url_for('admin.order_list'))
    orders = Order.query.filter_by(user_id=current_user.id).all()
    return render_template('order_list.html', orders=orders)