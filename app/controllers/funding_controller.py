from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from app.models.funding import Funding
from app.forms import FundingCreateForm
from datetime import datetime

funding_bp = Blueprint('funding', __name__)

@funding_bp.route('/fundings')
def funding_list():
    fundings = Funding.query.all()
    return render_template('funding_list.html', fundings=fundings)

@funding_bp.route('/fundings/<int:funding_id>')
def funding_detail(funding_id):
    funding = Funding.query.get_or_404(funding_id)
    return render_template('funding_detail.html', funding=funding)

@funding_bp.route('/fundings/create', methods=['GET', 'POST'])
def funding_create():
    form = FundingCreateForm()
    if form.validate_on_submit():
        funding = Funding(
            title=form.title.data,
            description=form.description.data,
            goal_amount=form.goal_amount.data,
            start_date=form.start_date.data,
            end_date=form.end_date.data,
            creator_id=current_user.id
        )
        db.session.add(funding)
        db.session.commit()
        flash('Funding created successfully.', 'success')
        return redirect(url_for('funding.funding_detail', funding_id=funding.id))
    return render_template('funding_create.html', form=form)

@funding_bp.route('/fundings/<int:funding_id>/edit', methods=['GET', 'POST'])
def funding_edit(funding_id):
    funding = Funding.query.get_or_404(funding_id)
    if funding.creator != current_user:
        flash('You are not authorized to edit this funding.', 'danger')
        return redirect(url_for('funding.funding_detail', funding_id=funding.id))
    form = FundingCreateForm(obj=funding)
    if form.validate_on_submit():
        form.populate_obj(funding)
        db.session.commit()
        flash('Funding updated successfully.', 'success')
        return redirect(url_for('funding.funding_detail', funding_id=funding.id))
    return render_template('funding_edit.html', form=form, funding=funding)

@funding_bp.route('/fundings/<int:funding_id>/delete', methods=['POST'])
def funding_delete(funding_id):
    funding = Funding.query.get_or_404(funding_id)
    if funding.creator != current_user:
        flash('You are not authorized to delete this funding.', 'danger')
        return redirect(url_for('funding.funding_detail', funding_id=funding.id))
    db.session.delete(funding)
    db.session.commit()
    flash('Funding deleted successfully.', 'success')
    return redirect(url_for('funding.funding_list'))

@funding_bp.route('/fundings/<int:funding_id>/participate', methods=['POST'])
def funding_participate(funding_id):
    funding = Funding.query.get_or_404(funding_id)
    amount = request.form.get('amount', type=int)
    if not amount:
        flash('Invalid participation amount.', 'danger')
        return redirect(url_for('funding.funding_detail', funding_id=funding.id))
    # TODO: Process user's participation
    flash('Thank you for your participation!', 'success')
    return redirect(url_for('funding.funding_detail', funding_id=funding.id))