from app import db
from app.models.user import User
from app.models.product import Product

class Gift(db.Model):
    __tablename__ = 'gifts'
    
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    message = db.Column(db.Text)
    sent_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    
    sender = db.relationship('User', foreign_keys=[sender_id], backref=db.backref('sent_gifts', lazy=True))
    receiver = db.relationship('User', foreign_keys=[receiver_id], backref=db.backref('received_gifts', lazy=True))
    product = db.relationship('Product', backref=db.backref('gifts', lazy=True))
    
    def __repr__(self):
        return f'<Gift {self.id}>'
    
    @classmethod
    def has_received(cls, user_id, product):
        return cls.query.filter_by(receiver_id=user_id, product_id=product.id).first() is not None