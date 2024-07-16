from src.models import db, Message, User


def record_message(chat_id, sender_id, content):
    new_message = Message(
        chat_id=chat_id,
        sender_id=sender_id,
        content=content,
    )

    db.session.add(new_message)
    db.session.commit()
    return new_message


def get_message(chat_id):

    messages_query = Message.query.filter(Message.chat_id == chat_id).order_by(Message.timestamp).all()
    messages = [{'username': User.query.filter_by(id=message.sender_id).first().username,
                 'content': message.content,
                 'timestamp': message.timestamp.strftime("%m/%d/%Y, %H:%M:%S")} for message in messages_query]
    print(messages)
    return messages

