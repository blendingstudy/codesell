from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models.review import Review
from app.models.product import Product
from app import db
from app.forms import ReviewForm

review_bp = Blueprint('review', __name__, url_prefix='/reviews')

@review_bp.route('/create/<int:product_id>', methods=['GET', 'POST'])
@login_required
def create_review(product_id):
    form = ReviewForm()
    product = Product.query.get_or_404(product_id)

    if form.validate_on_submit():
        rating = form.rating.data
        comment = form.comment.data

        review = Review(user_id=current_user.id, product_id=product.id, rating=rating, comment=comment)
        db.session.add(review)
        db.session.commit()

        flash('Review submitted successfully.', 'success')
        return redirect(url_for('product.get_product', product_id=product.id))

    return render_template('create_review.html', form=form, product=product)

@review_bp.route('/<int:review_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_review(review_id):
    review = Review.query.get_or_404(review_id)
    if review.user_id != current_user.id:
        flash('You are not authorized to edit this review.', 'warning')
        return redirect(url_for('product.get_product', product_id=review.product_id))

    form = ReviewForm()

    if form.validate_on_submit():
        review.rating = form.rating.data
        review.comment = form.comment.data
        db.session.commit()

        flash('Review updated successfully.', 'success')
        return redirect(url_for('product.get_product', product_id=review.product_id))

    form.rating.data = review.rating
    form.comment.data = review.comment

    return render_template('edit_review.html', form=form, review=review)

@review_bp.route('/<int:review_id>/delete', methods=['POST'])
@login_required
def delete_review(review_id):
    review = Review.query.get_or_404(review_id)
    if review.user_id != current_user.id:
        flash('You are not authorized to delete this review.', 'warning')
        return redirect(url_for('product.get_product', product_id=review.product_id))

    db.session.delete(review)
    db.session.commit()

    flash('Review deleted successfully.', 'success')
    return redirect(url_for('product.get_product', product_id=review.product_id))

@review_bp.route('/product/<int:product_id>')
def review_list(product_id):
    product = Product.query.get_or_404(product_id)
    reviews = Review.query.filter_by(product_id=product_id).all()
    return render_template('review_list.html', product=product, reviews=reviews)