from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
import requests
from app.models.cart import Cart, CartItem
from app.models.chat_room import ChatRoom
from app.models.funding import Funding
from app.models.order import OrderItem
from app.models.product import Product
from app.models.user import User
from app import db
from app.forms import RegistrationForm, LoginForm
from urllib.parse import urlparse
from config import Config

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        
        user = User.query.filter((User.username == username) | (User.email == email)).first()
        if user:
            flash('Username or email already exists', 'error')
            return redirect(url_for('auth.register'))
        
        new_user = User(username=username, email=email)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        
        #return redirect(url_for('product.index'))
        return redirect(url_for('auth.login'))
    else:
        flash('Please correct the errors below.', 'error')
    
    return render_template('register.html', title='Register', form=form)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        email = request.form['email']
        password = request.form['password']
        
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            #login_user(user, remember=form.remember_me.data)
            login_user(user)
            flash('Login successful.', 'success')
            next_page = request.args.get('next')
            if not next_page or urlparse(next_page).netloc != '':
                if user.is_admin:
                    next_page = url_for('admin.index')
                else:
                    next_page = url_for('index')
            return redirect(next_page)
        else:
            flash('Invalid email or password.', 'error')
            return redirect(url_for('auth.login'))
    
    return render_template('login.html', title='Login', form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('index'))

@auth_bp.route('/kakao')
def kakao_login():
    client_id = Config.KAKAO_APP_KEY
    redirect_uri = Config.KAKAO_REDIRECT_URL
    kakao_auth_url = f'https://kauth.kakao.com/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code'
    return redirect(kakao_auth_url)

@auth_bp.route('/kakao/callback')
def kakao_callback():
    code = request.args.get('code')
    client_id = Config.KAKAO_APP_KEY
    redirect_uri = Config.KAKAO_REDIRECT_URL
    token_request_url = f'https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={client_id}&redirect_uri={redirect_uri}&code={code}'

    token_response = requests.post(token_request_url)
    access_token = token_response.json().get('access_token')

    user_info_url = 'https://kapi.kakao.com/v2/user/me'
    headers = {'Authorization': f'Bearer {access_token}'}
    user_info_response = requests.get(user_info_url, headers=headers)
    user_info = user_info_response.json()

    kakao_account = user_info['kakao_account']
    email = kakao_account['email']
    nickname = kakao_account['profile']['nickname']

    user = User.query.filter_by(email=email).first()
    if not user:
        user = User(email=email, nickname=nickname)
        db.session.add(user)
        db.session.commit()

    login_user(user)
    return redirect(url_for('index'))

@auth_bp.route('/naver')
def naver_login():
    client_id = Config.NAVER_CLIENT_ID
    redirect_uri = Config.NAVER_REDIRECT_URI
    state = 'RAMDOM_STATE'
    naver_auth_url = f'https://nid.naver.com/oauth2.0/authorize?response_type=code&client_id={client_id}&redirect_uri={redirect_uri}&state={state}'
    return redirect(naver_auth_url)

@auth_bp.route('/naver/callback')
def naver_callback():
    code = request.args.get('code')
    state = request.args.get('state')
    
    token_request_url = 'https://nid.naver.com/oauth2.0/token'
    token_request_data = {
        'grant_type': 'authorization_code',
        'client_id': Config.NAVER_CLIENT_ID,
        'client_secret': Config.NAVER_CLIENT_SECRET,
        'code': code,
        'state': state,
    }

    token_response = requests.post(token_request_url, data=token_request_data)
    access_token = token_response.json().get('access_token')

    user_info_url = 'https://openapi.naver.com/v1/nid/me'
    headers = {'Authorization': f'Bearer {access_token}'}
    user_info_response = requests.get(user_info_url, headers=headers)
    user_info = user_info_response.json().get('response')

    email = user_info['email']
    nickname = user_info['nickname']

    user = User.query.filter_by(email=email).first()
    if not user:
        user = User(email=email, nickname=nickname)
        db.session.add(user)
        db.session.commit()

    login_user(user)
    return redirect(url_for('index'))

@auth_bp.route('/delete_account', methods=['POST'])
@login_required
def delete_account():
    user = User.query.get(current_user.id)
    # 사용자의 장바구니 아이템 삭제
    CartItem.query.filter_by(user_id=user.id).delete()
    Cart.query.filter_by(user_id=user.id).delete()

    # 사용자의 주문 삭제
    for order in user.orders:
        OrderItem.query.filter_by(order_id=order.id).delete()
        db.session.delete(order)

    #후원/상품의 판매자/피후원자 아이디가 NULL일 경우 판매/후원중지로 수정 필요
    for product in user.products:
        product.is_active = False      

    for funding in user.fundings:
        funding.is_active = False

    db.session.delete(user)
    db.session.commit()

    flash('Your account has been deleted.', 'success')
    return redirect(url_for('index'))

@auth_bp.route('/profile/<int:user_id>')
@login_required
def user_profile(user_id):
    user = User.query.get_or_404(user_id)
    products = user.products
    return render_template('user_profile.html', user=user, products=products)

""" @auth_bp.route('/seller/<int:user_id>')
def seller_info(user_id):
    user = User.query.get_or_404(user_id)
    products = user.products
    return render_template('seller_info.html', user=user, products=products) """
