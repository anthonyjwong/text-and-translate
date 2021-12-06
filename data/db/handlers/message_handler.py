from datetime import datetime

from db.models import Message
from db.sqlalchemy_db import create_session


def get_message_by_id(id: str, serialize=True):
    """
    Get message by primary key
    :param id: UUID
    :return: JSON
    """
    with create_session() as session:
        message = session.get(Message, id)
        if message == None:
            return None
        elif serialize:
            message = message.serialize
        return message


def get_conversation(user_1: str, user_2: str, serialize: bool = True):
    """
    Get message list by sender and receiver.
    :param sender: UUID
    :param receiver: UUID
    :return: JSON
    """
    with create_session() as session:
        messages = session.query(Message).filter(
            Message.sender == user_1 and Message.receiver == user_2).all()
        messages += session.query(Message).filter(
            Message.sender == user_2 and Message.receiver == user_1).all()

        if messages == None:
            return None
        return [message.serialize if serialize else message for message in messages]


def get_all_messages():
    """
    Get all messages
    :return: JSON
    """
    with create_session() as session:
        messages = session.query(Message).all()
        return [message.serialize for message in messages]


def create_message(sender: str, receiver: str, sent_at: datetime, message_content: str, serialize: bool = True):
    """
    Create a new message based on an associated name
    :param name: ex. "AJ Wong"
    :return: JSON (new stock) or raise RuntimeError if already exists
    """
    with create_session() as session:
        try:
            message = Message(sender=sender, receiver=receiver,
                              sent_at=sent_at, message_content=message_content)
            session.add(message)
            # must commit before new message can be fetched from DB table
            session.commit()
            return message.serialize if serialize else message
        except Exception as e:
            raise e


def delete_message_by_id(id: str):
    """
    Delete a message using a primary key ID
    :param id: UUID
    """
    with create_session() as session:
        message = get_message_by_id(id=id, serialize=False)
        if not message:
            raise RuntimeError(
                f"Cannot delete nonexistent message with ID {id}")
        session.delete(message)
        session.commit()
