from app import db
from app.models import BaseModel
from app.models.user import User
from app.models.product import Product

class Order(BaseModel):
    __tablename__ = 'orders'

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), nullable=False, default='pending')
    shipping_address = db.Column(db.String(255), nullable=False)

    user = db.relationship('User', backref=db.backref('orders', lazy=True))
    order_items = db.relationship('OrderItem', backref='order', lazy=True)

    def __init__(self, user_id, total_amount, shipping_address):
        self.user_id = user_id
        self.total_amount = total_amount
        self.shipping_address = shipping_address

    def __repr__(self):
        return f'<Order {self.id}>'
    
    @classmethod
    def has_purchased(cls, user_id, product):
        return cls.query.join(OrderItem).filter(
            cls.user_id == user_id,
            cls.status == 'paid',
            OrderItem.product_id == product.id
        ).scalar() is not None

class OrderItem(BaseModel):
    __tablename__ = 'order_items'

    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)

    product = db.relationship('Product', backref=db.backref('order_items', lazy=True))

    def __init__(self, order_id, product_id, quantity, price):
        self.order_id = order_id
        self.product_id = product_id
        self.quantity = quantity
        self.price = price

    def __repr__(self):
        return f'<OrderItem {self.id}>'