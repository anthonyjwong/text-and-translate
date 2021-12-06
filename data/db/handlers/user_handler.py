from db.models import User
from db.sqlalchemy_db import create_session


def get_user_by_id(id: str, serialize=True):
    """
    Get user by primary key
    :param id: UUID
    :return: JSON
    """
    with create_session() as session:
        user = session.get(User, id)
        if user == None:
            return None
        elif serialize:
            user = user.serialize
        return user


def get_user_by_name(name: str):
    """
    Get user by name.
    :param name: ex. "AJ Wong"
    :return: JSON or raise RuntimeException if not found
    """
    with create_session() as session:
        user = session.query(User).filter(User.name == name).first()
        return user.serialize if user else None


def get_all_users():
    """
    Get all users
    :return: JSON
    """
    with create_session() as session:
        users = session.query(User).all()
        return [user.serialize for user in users]


def create_user(name: str):
    """
    Create a new user based on an associated name
    :param name: ex. "AJ Wong"
    :return: JSON (new stock) or raise RuntimeError if already exists
    """
    with create_session() as session:
        try:
            user = User(name=name)
            session.add(user)
            # must commit before new user can be fetched from DB table
            session.commit()
            return get_user_by_name(name=name)
        except Exception as e:
            raise e


def delete_user_by_id(id: str):
    """
    Delete a user using a primary key ID
    :param id: UUID
    """
    with create_session() as session:
        user = get_user_by_id(id=id, serialize=False)
        if not user:
            raise RuntimeError(f"Cannot delete nonexistent user with ID {id}")
        session.delete(user)
        session.commit()
