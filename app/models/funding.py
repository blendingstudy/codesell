from app import db
from app.models import BaseModel
from app.models.user import User
from app.models.product import Product

class Funding(BaseModel):
    __tablename__ = 'fundings'

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), nullable=False, default='pending')

    user = db.relationship('User', backref=db.backref('fundings', lazy=True))
    product = db.relationship('Product', backref=db.backref('fundings', lazy=True))

    def __init__(self, user_id, product_id, amount):
        self.user_id = user_id
        self.product_id = product_id
        self.amount = amount

    def __repr__(self):
        return f'<Funding {self.id}>'