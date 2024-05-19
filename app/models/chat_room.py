from app import db
from datetime import datetime

class ChatRoom(db.Model):
   __tablename__ = 'chat_rooms'
   id = db.Column(db.Integer, primary_key=True)
   created_at = db.Column(db.DateTime, default=datetime.utcnow)
   user1_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
   user2_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
   
   user1 = db.relationship('User', foreign_keys=[user1_id], backref=db.backref('chat_rooms_as_user1', lazy=True))
   user2 = db.relationship('User', foreign_keys=[user2_id], backref=db.backref('chat_rooms_as_user2', lazy=True))
   
   def __init__(self, user1_id, user2_id):
       self.user1_id = user1_id
       self.user2_id = user2_id
   
   def __repr__(self):
       return f'<ChatRoom {self.id}>'