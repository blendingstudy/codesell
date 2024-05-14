from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from app.models.chat_room import ChatRoom
from app.models.chat_message import ChatMessage
from app import db

chat_bp = Blueprint('chat', __name__, url_prefix='/chat')

@chat_bp.route('/')
@login_required
def chat_list():
    chat_rooms = current_user.chat_rooms
    return render_template('chat/chat_list.html', chat_rooms=chat_rooms)

@chat_bp.route('/create', methods=['POST'])
@login_required
def create_chat_room():
    name = request.form['name']
    chat_room = ChatRoom(name=name)
    chat_room.users.append(current_user)
    db.session.add(chat_room)
    db.session.commit()
    return jsonify({'status': 'success', 'chat_room_id': chat_room.id})

@chat_bp.route('/room/<int:chat_room_id>')
@login_required
def chat_room(chat_room_id):
    chat_room = ChatRoom.query.get_or_404(chat_room_id)
    if current_user not in chat_room.users:
        chat_room.users.append(current_user)
        db.session.commit()
    messages = ChatMessage.query.filter_by(chat_room_id=chat_room_id).order_by(ChatMessage.timestamp.asc()).all()
    return render_template('chat/chat_room.html', chat_room=chat_room, messages=messages)

@chat_bp.route('/send_message', methods=['POST'])
@login_required
def send_message():
    chat_room_id = request.form['chat_room_id']
    content = request.form['content']
    chat_message = ChatMessage(content=content, user_id=current_user.id, chat_room_id=chat_room_id)
    db.session.add(chat_message)
    db.session.commit()
    return jsonify({'status': 'success', 'message': chat_message.to_dict()})

@chat_bp.route('/get_messages/<int:chat_room_id>')
@login_required
def get_messages(chat_room_id):
    last_message_id = request.args.get('last_message_id', 0, type=int)
    messages = ChatMessage.query.filter(
        ChatMessage.chat_room_id == chat_room_id,
        ChatMessage.id > last_message_id
    ).order_by(ChatMessage.timestamp.asc()).all()
    return jsonify({'status': 'success', 'messages': [message.to_dict() for message in messages]})