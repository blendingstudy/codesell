from flask import render_template, request, session, redirect, url_for, flash
from codesell.models import User
from codesell import db
from codesell.form import RegisterForm, LoginForm
from flask_login import login_user, logout_user, login_required

def login():
    if request.method == 'POST':
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user and user.check_password(form.password.data):
                login_user(user)
                flash('Login successful!', 'success')
                return redirect(url_for('main.index'))
            else:
                flash('Invalid email or password', 'danger')
    else:
        form = LoginForm()
    return render_template('login.html', form=form)

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

@login_required
def logout():
    logout_user()
    session.clear()
    flash('You have been logged out.', 'success')
    return redirect(url_for('main.index'))