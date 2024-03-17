""" import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__)))) """

from . import auth_bp
from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from controllers.auth_controller import authenticate_user, register_user
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from models import User, db
from form import RegisterForm, LoginForm
from __init__ import app

login_manager = LoginManager(app)  # LoginManager 초기화
login_manager.login_view = 'auth.login'  # 로그인 페이지 설정

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid email or password', 'danger')
    return render_template('login.html', form=form)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data
        )
        db.session.add(user)
        db.session.commit()
        flash('Registration successful!', 'success')
        return redirect(url_for('auth.login'))
    return render_template('register.html', form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('index'))