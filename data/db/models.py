
from datetime import datetime
from uuid import uuid4

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import validates
from sqlalchemy.sql.sqltypes import Text

from db.sqlalchemy_db import create_table, get_engine

Base = declarative_base()


def p_key_column(use_int: bool = False):
    if use_int:
        return Column(Integer, primary_key=True)
    else:
        return Column(UUID(as_uuid=True), primary_key=True, default=uuid4)


def f_key_column(
        column_attribute: str,
        use_int: bool = False,
        on_delete: str = "CASCADE",
        on_update: str = "CASCADE",
        nullable: bool = False,
):
    if use_int:
        type = Integer
    else:
        type = UUID(as_uuid=True)
    return Column(
        type,
        ForeignKey(column_attribute, ondelete=on_delete, onupdate=on_update),
        nullable=nullable,
    )


def get_datettime():
    return datetime.now()


class User(Base):
    __tablename__ = "user"

    id = p_key_column()
    name = Column(String)
    lang = Column(String)

    @property
    def serialize(self):
        """
        Return JSON serialized version of Stock instance
        @return: JSON
        """
        return {
            "id": self.id,
            "name": self.name,
            "lang": self.lang
        }


class Message(Base):
    __tablename__ = "message"

    id = p_key_column()
    sender = f_key_column("user.id")
    receiver = f_key_column("user.id")
    sent_at = Column(DateTime, default=get_datettime)
    message_content = Column(String)
    lang = Column(String)

    @property
    def serialize(self):
        """
        Return JSON serialized version of Stock instance
        @return: JSON
        """
        return {
            "id": self.id,
            "sender": self.sender,
            "receiver": self.receiver,
            "sent_at": self.sent_at,
            "message_content": self.message_content,
            "lang": self.lang
        }


def instantiate_tables():
    """
    Define all tables, should be called only once
    """
    print("instantiating db tables...")
    for table in [User, Message]:
        create_table(table)
