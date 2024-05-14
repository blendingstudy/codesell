from app import db
from datetime import datetime

class ChatRoom(db.Model):
    __tablename__ = 'chat_rooms'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # 채팅방과 사용자 간의 다대다 관계 정의
    users = db.relationship('User', secondary='chat_room_users', backref='chat_rooms')
    
    def __init__(self, name):
        self.name = name
    
    def __repr__(self):
        return f'<ChatRoom {self.name}>'

# 채팅방과 사용자 간의 다대다 관계를 위한 연결 테이블 정의
chat_room_users = db.Table('chat_room_users',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('chat_room_id', db.Integer, db.ForeignKey('chat_rooms.id'), primary_key=True)
)