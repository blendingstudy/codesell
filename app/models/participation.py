from app import db
from datetime import datetime
#from app.models.funding import Funding  # Funding 모델 import 추가

class Participation(db.Model):
    __tablename__ = 'participations'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='SET NULL'))
    funding_id = db.Column(db.Integer, db.ForeignKey('fundings.id'), nullable=False)  # 외래 키 제약 조건 추가
    amount = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    user = db.relationship('User', backref=db.backref('participations', lazy=True))
    funding = db.relationship('Funding', backref=db.backref('participations', lazy=True))
    
    def __init__(self, user_id, funding_id, amount):
        self.user_id = user_id
        self.funding_id = funding_id
        self.amount = amount
    
    def __repr__(self):
        return f'<Participation {self.id}>'