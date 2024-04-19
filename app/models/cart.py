from app import db
from app.models import BaseModel
from app.models.user import User
from app.models.product import Product

class CartItem(BaseModel):
    __tablename__ = 'cart_items'

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    cart_id = db.Column(db.Integer, db.ForeignKey('carts.id'), nullable=False)

    user = db.relationship('User', backref=db.backref('cart_items', lazy=True))
    product = db.relationship('Product', backref=db.backref('cart_items', lazy=True))

    def __init__(self, user_id, product_id, cart_id, quantity=1):
        self.user_id = user_id
        self.product_id = product_id
        self.quantity = quantity
        self.cart_id = cart_id

    def __repr__(self):
        return f'<CartItem {self.id}>'

class Cart(BaseModel):
    __tablename__ = 'carts'

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('cart', uselist=False, lazy=True))

    items = db.relationship('CartItem', backref='cart', lazy=True)

    def __init__(self, user_id):
        self.user_id = user_id

    def add_item(self, product_id, quantity=1, cart_id=None):
        if not cart_id:
            cart_id = self.id
        cart_item = CartItem.query.filter_by(user_id=self.user_id, product_id=product_id).first()
        if cart_item:
            cart_item.quantity += quantity
        else:
            cart_item = CartItem(user_id=self.user_id, product_id=product_id, cart_id=cart_id, quantity=quantity)
            db.session.add(cart_item)
        db.session.commit()

    def remove_item(self, product_id):
        cart_item = CartItem.query.filter_by(user_id=self.user_id, product_id=product_id).first()
        if cart_item:
            db.session.delete(cart_item)
            db.session.commit()

    def clear(self):
        CartItem.query.filter_by(user_id=self.user_id).delete()
        db.session.commit()

    def get_total_price(self):
        total_price = 0
        cart_items = CartItem.query.filter_by(user_id=self.user_id).all()
        for item in cart_items:
            total_price += item.product.price * item.quantity
        return total_price

    def __repr__(self):
        return f'<Cart {self.id}>'