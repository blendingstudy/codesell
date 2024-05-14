from flask import request
from flask_socketio import SocketIO, emit, join_room, leave_room
from app.models.chat_message import ChatMessage
from app.models.chat_room import ChatRoom
from app.models.user import User
from app import db

socketio = SocketIO()

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

@socketio.on('join_room')
def handle_join_room(data):
    user_id = data['user_id']
    chat_room_id = data['chat_room_id']
    join_room(chat_room_id)
    print(f'User {user_id} joined room {chat_room_id}')

@socketio.on('leave_room')
def handle_leave_room(data):
    user_id = data['user_id']
    chat_room_id = data['chat_room_id']
    leave_room(chat_room_id)
    print(f'User {user_id} left room {chat_room_id}')

@socketio.on('send_message')
def handle_send_message(data):
    chat_room_id = data['chat_room_id']
    user_id = data['user_id']
    message = data['message']

    user = User.query.get(user_id)
    chat_room = ChatRoom.query.get(chat_room_id)

    if user and chat_room:
        chat_message = ChatMessage(content=message, user_id=user_id, chat_room_id=chat_room_id)
        db.session.add(chat_message)
        db.session.commit()

        emit('receive_message', chat_message.to_dict(), room=chat_room_id)