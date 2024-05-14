from app import db
from datetime import datetime

class ChatMessage(db.Model):
    __tablename__ = 'chat_messages'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    chat_room_id = db.Column(db.Integer, db.ForeignKey('chat_rooms.id'), nullable=False)
    
    user = db.relationship('User', backref='chat_messages')
    chat_room = db.relationship('ChatRoom', backref='chat_messages')
    
    def __init__(self, content, user_id, chat_room_id):
        self.content = content
        self.user_id = user_id
        self.chat_room_id = chat_room_id
    
    def __repr__(self):
        return f'<ChatMessage {self.id}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'content': self.content,
            'timestamp': self.timestamp.isoformat(),
            'user_id': self.user_id,
            'chat_room_id': self.chat_room_id,
            'username': self.user.username
        }