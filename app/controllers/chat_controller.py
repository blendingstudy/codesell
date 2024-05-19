from flask import Blueprint, redirect, render_template, request, jsonify, url_for
from flask_login import login_required, current_user
from app.models.chat_room import ChatRoom
from app.models.chat_message import ChatMessage
from app import db
from app.models.user import User
from app.socket_io import socketio

chat_bp = Blueprint('chat', __name__, url_prefix='/chat')

@chat_bp.route('/')
@login_required
def chat_list():
    chat_rooms = ChatRoom.query.filter(
        db.or_(
            ChatRoom.user1_id == current_user.id,
            ChatRoom.user2_id == current_user.id
        )
    ).all()
    return render_template('chat_list.html', chat_rooms=chat_rooms)

@chat_bp.route('/room/<int:chat_room_id>')
@login_required
def chat_room(chat_room_id):
    chat_room = ChatRoom.query.get_or_404(chat_room_id)
    if current_user.id != chat_room.user1_id and current_user.id != chat_room.user2_id:
        return "Access denied", 403
    messages = ChatMessage.query.filter_by(chat_room_id=chat_room_id).order_by(ChatMessage.timestamp.asc()).all()
    return render_template('chat_room.html', chat_room=chat_room, messages=messages)

@chat_bp.route('/send_message', methods=['POST'])
@login_required
def send_message():
    chat_room_id = request.form['chat_room_id']
    content = request.form['content']
    chat_message = ChatMessage(content=content, user_id=current_user.id, chat_room_id=chat_room_id)
    db.session.add(chat_message)
    db.session.commit()
    
    message_data = {
        'id': chat_message.id,
        'content': chat_message.content,
        'user_id': chat_message.user_id,
        'username': chat_message.user.username,
        'chat_room_id': chat_message.chat_room_id,
        'timestamp': chat_message.timestamp.strftime('%Y-%m-%d %H:%M:%S')
    }
    
    return jsonify({'status': 'success', 'message': message_data})

@chat_bp.route('/get_messages/<int:chat_room_id>')
@login_required
def get_messages(chat_room_id):
    last_message_id = request.args.get('last_message_id', 0, type=int)
    messages = ChatMessage.query.filter(
        ChatMessage.chat_room_id == chat_room_id,
        ChatMessage.id > last_message_id
    ).order_by(ChatMessage.timestamp.asc()).all()
    
    message_data = []
    for message in messages:
        message_data.append({
            'id': message.id,
            'content': message.content,
            'user_id': message.user_id,
            'username': message.user.username,
            'chat_room_id': message.chat_room_id,
            'timestamp': message.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        })
    
    return jsonify({'status': 'success', 'messages': message_data})

@chat_bp.route('/start_chat/<int:user_id>', methods=['POST'])
@login_required
def start_chat(user_id):
    user = User.query.get_or_404(user_id)
    chat_room = ChatRoom.query.filter(
        db.or_(
            db.and_(ChatRoom.user1_id == current_user.id, ChatRoom.user2_id == user.id),
            db.and_(ChatRoom.user1_id == user.id, ChatRoom.user2_id == current_user.id)
        )
    ).first()
    if not chat_room:
        chat_room = ChatRoom(user1_id=current_user.id, user2_id=user.id)
        db.session.add(chat_room)
        db.session.commit()
    return redirect(url_for('chat.chat_room', chat_room_id=chat_room.id))