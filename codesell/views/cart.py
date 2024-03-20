from flask import render_template, request, redirect, url_for, session
from codesell.models import Product

def add_to_cart(product_id):
    quantity = int(request.form['quantity'])
    product = Product.query.get(product_id)
    if 'cart' not in session:
        session['cart'] = []
    session['cart'].append({'id': product.id, 'name': product.name, 'price': product.price, 'quantity': quantity})
    session.modified = True
    return redirect(url_for('product.product_detail', product_id=product_id))
    #추후에 장바구니 페이지와 현재 페이지 중 사용자가 선택할 수 있게 변경

def remove_from_cart(product_id):
    cart = session['cart']
    for item in cart:
        if item['id'] == product_id:
            cart.remove(item)
            break
    session.modified = True
    return redirect(url_for('cart.view_cart'))

def view_cart():
    cart = session.get('cart', [])
    total_price = sum(item['price'] * item['quantity'] for item in cart)
    return render_template('cart.html', cart=cart, total_price=total_price)

def checkout():
    # 결제 처리 로직 구현
    # 결제 완료 후 장바구니 비우기
    session['cart'] = []
    session.modified = True
    return redirect(url_for('main.index'))