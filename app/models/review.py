from app import db
from sqlalchemy import func
from app.models import BaseModel

class Review(BaseModel):
    __tablename__ = 'reviews'

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text)

    user = db.relationship('User', backref=db.backref('reviews', lazy=True))
    product = db.relationship('Product', backref=db.backref('reviews', lazy=True))

    def __init__(self, user_id, product_id, rating, comment=None):
        self.user_id = user_id
        self.product_id = product_id
        self.rating = rating
        self.comment = comment

    def __repr__(self):
        return f'<Review {self.id}>'

    @classmethod
    def get_average_rating(cls, product_id):
        avg_rating = db.session.query(func.avg(cls.rating)).filter_by(product_id=product_id).scalar()
        return round(avg_rating, 2) if avg_rating else 0