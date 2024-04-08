from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models.funding import Funding
from app.models.product import Product
from app import db

funding_bp = Blueprint('funding', __name__, url_prefix='/fundings')

@funding_bp.route('/')
def funding_list():
    fundings = Funding.query.all()
    return render_template('funding.html', fundings=fundings)

@funding_bp.route('/<int:funding_id>')
def funding_detail(funding_id):
    funding = Funding.query.get_or_404(funding_id)
    return render_template('funding/detail.html', funding=funding)

@funding_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_funding():
    if request.method == 'POST':
        product_id = request.form['product_id']
        amount = float(request.form['amount'])

        product = Product.query.get_or_404(product_id)

        funding = Funding(user_id=current_user.id, product_id=product_id, amount=amount)
        db.session.add(funding)
        db.session.commit()

        flash('Funding created successfully.', 'success')
        return redirect(url_for('funding.funding_detail', funding_id=funding.id))

    products = Product.query.all()
    return render_template('funding.html', products=products)

@funding_bp.route('/<int:funding_id>/update', methods=['GET', 'POST'])
@login_required
def update_funding(funding_id):
    funding = Funding.query.get_or_404(funding_id)

    if funding.user_id != current_user.id:
        flash('You do not have permission to update this funding.', 'error')
        return redirect(url_for('funding.funding_detail', funding_id=funding.id))

    if request.method == 'POST':
        funding.amount = float(request.form['amount'])
        db.session.commit()

        flash('Funding updated successfully.', 'success')
        return redirect(url_for('funding.funding_detail', funding_id=funding.id))

    return render_template('funding/update.html', funding=funding)

@funding_bp.route('/<int:funding_id>/delete', methods=['POST'])
@login_required
def delete_funding(funding_id):
    funding = Funding.query.get_or_404(funding_id)

    if funding.user_id != current_user.id:
        flash('You do not have permission to delete this funding.', 'error')
        return redirect(url_for('funding.funding_detail', funding_id=funding.id))

    db.session.delete(funding)
    db.session.commit()

    flash('Funding deleted successfully.', 'success')
    return redirect(url_for('funding.funding_list'))