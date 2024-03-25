from flask import Blueprint, request, jsonify, flash, redirect, url_for
from iamport import Iamport
from codesell.models import Order, OrderItem
import config

order_bp = Blueprint('order', __name__, url_prefix='/order')
iamport = Iamport(imp_key=config.IAMP_KEY, imp_secret=config.IAMP_SECRET)

order_bp.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if request.mothod == 'POST':
        # 주문 정보 생성
        order = Order(
            buyer_email=request.form['buyer_email'],
            buyer_name=request.form['buyer_name'],
            buyer_tel=request.form['buyer_tel'],
            buyer_addr=request.form['buyer_addr'],
            buyer_postcode=request.form['buyer_postcode']
        )
        order.save()

        # 주문 상품 정보 생성
        cart_items = request.form.getlist('cart_items')
        for item in cart_items:
            product_id, quantity = item.split(':')
            order_item = OrderItem(order=order, product_id=product_id, quantity=quantity)
            order_item.save()

        # 결제 프로세스 진행
        result = process_payment(order)
        if result['status'] == 'paid':
            update_order_status(order, 'paid')
            flash('결제가 완료되었습니다.')
            return redirect(url_for('order.order_complete', order_id=order.id))
        else:
            update_order_status(order, 'failed')
            flash('결제에 실패하였습니다.')
            return redirect(url_for('order.checkout'))

@order_bp.route('/order_complete/<int:order_id>')
def order_complete


@order_bp.route('/process_payment', methods=['POST'])
def process_payment():
    order_id = request.form['order_id']
    order = Order.query.get(order_id)
    
    try:
        response = iamport.pay_onetime(
            merchant_uid=order.id,
            name='상품 결제',
            amount=order.get_total_amount(),
            buyer_email=order.buyer_email,
            buyer_name=order.buyer_name,
            buyer_tel=order.buyer_tel,
            buyer_addr=order.buyer_addr,
            buyer_postcode=order.buyer_postcode
        )
        return jsonify(response)
    except Iamport.ResponseError as e:
        return jsonify({'status': 'failed', 'message': e.message})
    except Iamport.HttpError as http_error:
        return jsonify({'status': 'failed', 'message': http_error.reason})

@order_bp.route('/update_order_status', methods=['POST'])
def update_order_status():
    order_id = request.form['order_id']
    status = request.form['status']
    order = Order.query.get(order_id)
    order.status = status
    order.save()
    return jsonify({'message': 'Order status updated'})