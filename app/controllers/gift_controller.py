from flask import Blueprint, jsonify, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models.cart import CartItem
from app.models.gift import Gift
from app.models.user import User
from app.models.product import Product
from app.forms import GiftForm

gift_bp = Blueprint('gift', __name__, url_prefix='/gifts')

@gift_bp.route('/send/<int:product_id>', methods=['GET', 'POST'])
@login_required
def send_gift(product_id):
    product = Product.query.get_or_404(product_id)
    form = GiftForm()
    
    if form.validate_on_submit():
        receiver_email = form.receiver_email.data
        message = form.message.data
        
        receiver = User.query.filter_by(email=receiver_email).first()
        if not receiver:
            flash('받는 사람의 이메일이 올바르지 않습니다.', 'error')
            return redirect(url_for('gift.send_gift', product_id=product.id))
        
        gift = Gift(sender=current_user, receiver=receiver, product=product, message=message)
        db.session.add(gift)
        db.session.commit()
        
        flash('선물이 성공적으로 전송되었습니다.', 'success')
        return jsonify({'success': True, 'redirect_url': url_for('product.get_product', product_id=product.id)})
    
    return render_template('gift_send.html', product=product, form=form)

@gift_bp.route('/list')
@login_required
def gift_list():
    received_gifts = current_user.received_gifts
    sent_gifts = current_user.sent_gifts
    return render_template('gift_list.html', received_gifts=received_gifts, sent_gifts=sent_gifts)
