from flask import Blueprint, render_template, redirect, request, url_for, flash
from flask_login import login_required, current_user
from app.models.order import Order
from app.models.cart import CartItem
from app import db

mypage_bp = Blueprint('mypage', __name__, url_prefix='/mypage')

@mypage_bp.route('/')
@login_required
def index():
    orders = Order.query.filter_by(user_id=current_user.id).all()
    cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
    return render_template('mypage_index.html', orders=orders, cart_items=cart_items)

@mypage_bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    if request.method == 'POST':
        current_user.username = request.form['username']
        current_user.email = request.form['email']
        db.session.commit()
        flash('Profile updated successfully.', 'success')
        return redirect(url_for('mypage.index'))
    return render_template('edit_profile.html', user=current_user)