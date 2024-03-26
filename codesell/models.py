from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from codesell import db
#from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    #password_hash = db.Column(db.String(128), nullable=False)

    """ @property
    def password(self):
        raise AttributeError('password is not a readable attribute') """

    """ @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password) """

    def check_password(self, password):
        #return check_password_hash(self.password_hash, password)
        return self.password == password

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    price = db.Column(db.Integer, nullable=False)

class FundingProject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    goal = db.Column(db.Integer, nullable=False)
    current_amount = db.Column(db.Integer, default=0)
    end_date = db.Column(db.String(120), nullable=False)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    buyer_email = db.Column(db.String(120), nullable=False)
    buyer_name = db.Column(db.String(120), nullable=False)
    buyer_tel = db.Column(db.String(20), nullable=False)
    buyer_addr = db.Column(db.String(200), nullable=False)
    buyer_postcode = db.Column(db.String(20), nullable=False)
    status = db.Column(db.String(20), default='pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    items = db.relationship('OrderItem', backref='order', lazy=True)

    def __init__(self, buyer_email, buyer_name, buyer_tel, buyer_addr, buyer_postcode):
        self.buyer_email = buyer_email
        self.buyer_name = buyer_name
        self.buyer_tel = buyer_tel
        self.buyer_addr = buyer_addr
        self.buyer_postcode = buyer_postcode

    def __repr__(self):
        return f'<Order {self.id}>'

    def get_total_amount(self):
        total = 0
        for item in self.items:
            total += item.get_subtotal()
        return total
    
    def save(self):
        db.session.add(self)
        db.session.commit()

class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

    def __init__(self, order, product_id, quantity):
        self.order = order
        self.product_id = product_id
        self.quantity = quantity

    def __repr__(self):
        return f'<OrderItem {self.id}>'

    def get_subtotal(self):
        product = Product.query.get(self.product_id)
        return product.price * self.quantity
    
    def save(self):
        db.session.add(self)
        db.session.commit()