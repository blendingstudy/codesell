from app import db
from app.models import BaseModel

class Product(BaseModel):
    __tablename__ = 'products'

    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    image_url = db.Column(db.String(200))
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    category = db.relationship('Category', backref=db.backref('products', lazy=True), foreign_keys=[category_id])
    language_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    language = db.relationship('Category', backref=db.backref('language_products', lazy=True), foreign_keys=[language_id])

    def __init__(self, name, description, price, quantity, image_url, category_id):
        self.name = name
        self.description = description
        self.price = price
        self.quantity = quantity
        self.image_url = image_url
        self.category_id = category_id

    def __repr__(self):
        return f'<Product {self.name}>'