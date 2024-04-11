from flask import Blueprint, jsonify, render_template, request, redirect, url_for, flash
from flask_login import current_user
from app import db
from app.models.funding import Funding
from app.models.participation import Participation
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
    data = request.get_json()
    if not data:
        return jsonify({'success': False, 'message': 'Invalid request data.'}), 400
    amount = data.get('amount')
    if not amount or amount <= 0:
        return jsonify({'success': False, 'message': 'Invalid participation amount.'}), 400
    
    # 펀딩 참여 로직 구현
    participation = Participation(user_id=current_user.id, funding_id=funding.id, amount=amount)
    funding.current_amount += amount
    db.session.add(participation)
    db.session.commit()
    
    if funding.is_funded():
        # 펀딩 목표 달성 시 추가 작업 수행
        funding.status = 'success'
        db.session.commit()
        # TODO: 펀딩 성공 시 필요한 추가 작업 수행 (예: 결제 처리, 알림 전송 등)
    
    return jsonify({'success': True, 'message': 'Thank you for your participation!'})