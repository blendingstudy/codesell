from app import db
from app.models import BaseModel
from app.models.review import Review
from app.models.user import User
from sqlalchemy import func

class Product(BaseModel):
    __tablename__ = 'products'

    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)
    code_file = db.Column(db.String(200), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    category = db.relationship('Category', backref=db.backref('products', lazy=True), foreign_keys=[category_id])
    language_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    language = db.relationship('Category', backref=db.backref('language_products', lazy=True), foreign_keys=[language_id])
    seller_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='SET NULL'), nullable=True)
    seller = db.relationship('User', backref=db.backref('products', lazy=True))
    is_active = db.Column(db.Boolean, default=True)
    demo_link = db.Column(db.String(255), nullable=True)

    def __init__(self, name, description, price, code_file, category_id, language_id, seller_id, demo_link):
        self.name = name
        self.description = description
        self.price = price
        self.code_file = code_file
        self.category_id = category_id
        self.language_id = language_id
        self.seller_id = seller_id
        self.demo_link = demo_link

    def __repr__(self):
        return f'<Product {self.name}>'
    
    def get_average_rating(self):
        avg_rating = db.session.query(func.avg(Review.rating)).filter_by(product_id=self.id).scalar()
        return round(avg_rating, 2) if avg_rating else 0