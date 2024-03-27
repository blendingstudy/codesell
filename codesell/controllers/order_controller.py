from flask import Blueprint, request, jsonify, flash, redirect, url_for
from iamport import Iamport
from codesell.models import Order, OrderItem
from codesell.views.order import checkout
import config

order_bp = Blueprint('order', __name__, url_prefix='/order')
iamport = Iamport(imp_key=config.IAMP_KEY, imp_secret=config.IAMP_SECRET)

order_bp.route('/checkout', methods=['GET', 'POST'])(checkout)

@order_bp.route('/process_payment', methods=['POST'])
def process_payment():
    print("order_controller")
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
        return jsonify({'status': 'failed', 'message': str(e)})
    except Iamport.HttpError as http_error:
        return jsonify({'status': 'failed', 'message': str(http_error)})
    except Exception as e:
        return jsonify({'status': 'failed', 'message': '결제 처리 중 오류가 발생했습니다.'})

@order_bp.route('/update_order_status', methods=['POST'])
def update_order_status():
    order_id = request.form['order_id']
    status = request.form['status']
    order = Order.query.get(order_id)
    order.status = status
    order.save()
    return jsonify({'message': 'Order status updated'})