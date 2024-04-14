from datetime import datetime
from app import db

class Funding(db.Model):
    __tablename__ = 'fundings'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    goal_amount = db.Column(db.Integer, nullable=False)
    current_amount = db.Column(db.Integer, default=0)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), default='ongoing')
    creator_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    creator = db.relationship('User', backref=db.backref('fundings', lazy=True))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __init__(self, title, description, goal_amount, start_date, end_date, creator_id):
        self.title = title
        self.description = description
        self.goal_amount = goal_amount
        self.start_date = start_date
        self.end_date = end_date
        self.creator_id = creator_id
    
    def __repr__(self):
        return f'<Funding {self.title}>'
    
    def update_status(self):
        if self.is_funded():
            self.status = 'success'
        elif not self.is_ongoing():
            self.status = 'fail'
        db.session.commit()
    
    def is_ongoing(self):
        current_date = datetime.utcnow().date()
        return self.start_date.date() <= current_date <= self.end_date.date()
    
    def is_funded(self):
        return self.current_amount >= self.goal_amount