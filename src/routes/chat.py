from flask import Blueprint, request, jsonify
from src.models import User, db, Chat
from src import socketio
from flask_socketio import join_room, leave_room, send
from src.service.message_service import record_message, get_message

chat_bp = Blueprint('chat', __name__)


@chat_bp.route('/search_user', methods=['GET'])
def search_user():
    username = request.args.get('username')
    chat_user = request.args.get('chatUser')
    print(username)
    if not username:
        return jsonify({'message': 'Username parameter is required'}), 400

    users = User.query.filter(User.username.like(f'%{username}%')).all()
    user_list = [{'uid': user.id, 'username': user.username, 'message': 'succeed'} for user in users if user.username != chat_user]
    print(user_list)

    return jsonify(user_list), 200


@chat_bp.route('/initiate_chat', methods=['POST'])
def initiate_chat():
    data = request.get_json()
    user_id = data.get('userId')
    recipient_id = data.get('recipientId')

    if not user_id or not recipient_id:
        return jsonify({'message': 'User ID and Recipient ID are required'}), 400

    user = User.query.get(user_id)
    recipient = User.query.get(recipient_id)

    if not user or not recipient:
        return jsonify({'message': 'User or Recipient not found'}), 404

    existing_chat: Chat = Chat.query.filter(
        (Chat.user_id == user_id) & (Chat.recipient_id == recipient_id) |
        (Chat.user_id == recipient_id) & (Chat.recipient_id == user_id)
    ).first()

    if existing_chat:
        return jsonify({'message': 'Chat already exists', 'cid': existing_chat.id})

    new_chat = Chat(user_id=user_id, recipient_id=recipient_id)
    db.session.add(new_chat)
    db.session.commit()

    return jsonify({'message': 'Chat initiated', 'cid': new_chat.id}), 201


@socketio.on('join')
def on_join(data):
    username = data['username']
    room = data['room']
    join_room(room)

    messages = get_message(int(room))
    for message in messages:
        send(message, to=room)

    send({'username': 'system', 'content': ' ^ ^ ^ ^ ^ Past Message ^ ^ ^ ^ ^ '}, to=room)

    # message = {'username': username, 'content': " has entered the room."}
    # send(message, to=room)


@socketio.on('leave')
def on_leave(data):
    username = data['username']
    room = data['room']
    leave_room(room)
    message = {'username': username, 'content': " has left the room."}
    send(message, to=room)


@socketio.on('message')
def handle_message(data):

    room = data['room']
    message = data['message']

    cid = int(data['room'])
    uid = int(message['uid'])
    content = message['content']

    recorded_message = record_message(cid, uid, content)
    print(type(recorded_message))

    send(message, to=room)
