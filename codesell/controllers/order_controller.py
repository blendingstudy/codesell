from flask import Blueprint, request, jsonify
from iamport import Iamport
from codesell.models import Order, OrderItem
from codesell.views.order import checkout, order_complete

order_bp = Blueprint('order', __name__, url_prefix='/order')
iamport = Iamport(imp_key='your_imp_key', imp_secret='your_imp_secret')

order_bp.route('/checkout', methods=['GET', 'POST'])(checkout)
order_bp.route('/order_complete/<int:order_id>')(order_complete)

def process_payment(order):
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
        return response
    except Iamport.ResponseError as e:
        return {'status': 'failed', 'message': e.message}
    except Iamport.HttpError as http_error:
        return {'status': 'failed', 'message': http_error.reason}

def update_order_status(order, status):
    order.status = status
    order.save()