from flask import render_template, request, redirect, url_for, flash, session
from codesell.models import Order, OrderItem
import requests

def checkout():
    cart_items = session.get('cart', [])
    if request.method == 'POST':
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
        for item in cart_items:
            order_item = OrderItem(order=order, product_id=item['id'], quantity=item['quantity'])
            order_item.save()

        # 결제 프로세스 진행
        result = process_payment(order)
        if result['status'] == 'paid':
            update_order_status(order, 'paid')
            flash('결제가 완료되었습니다.')
            return order_complete(order.id)
        else:
            update_order_status(order, 'failed')
            flash('결제에 실패하였습니다.')
            return redirect(url_for('order.checkout'))
    else:
        return render_template('checkout.html')

def order_complete(order_id):
    order = Order.query.get(order_id)
    return render_template('order_complete.html', order=order)

def process_payment(order):
    url = url_for('order.process_payment', _external=True)
    data = {'order_id': order.id}
    response = requests.post(url, data=data)
    print(response.json())
    return response.json()

def update_order_status(order, status):
    url = url_for('order.update_order_status', _external=True)
    data = {'order_id': order.id, 'status': status}
    response = requests.post(url, data=data)
    return response.json()