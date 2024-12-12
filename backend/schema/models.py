import sqlalchemy.types
from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, Text, Boolean, ForeignKeyConstraint
from sqlalchemy.orm import relationship

from backend.db.session import Base

class User(Base):
    __tablename__ = "user"

    user_id = Column(Integer, name="user_id", primary_key=True)
    first_name = Column(String(20), nullable=False, default="Mate")
    last_name = Column(String(20), nullable=False, default="Study")
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(100), nullable=False)
    chatroom = relationship("Chatroom", back_populates="user")

class Chatroom(Base):
    __tablename__ = "chatroom"

    chatroom_id = Column(Integer, name="chatroom_id", primary_key=True)
    chatroom_name = Column(String(50), nullable=False, default="Unnamed Chatroom")
    instructor_name = Column(String(20))
    course_code = Column(String(20))
    user_id = Column(Integer, ForeignKey("user.user_id"), nullable=False)
    user = relationship("User", back_populates="chatroom")
    message = relationship("Message", back_populates="chatroom", cascade="all, delete")
    document = relationship("Document", back_populates="chatroom", cascade="all, delete")

    __table_args__ = (
        ForeignKeyConstraint(
            ['user_id'], ['user.user_id'],
            name='chatroom_user_id_fkey',
            ondelete="CASCADE"
        ),
    )

class Message(Base):
    __tablename__ = "message"
    message_id = Column(Integer, primary_key=True)
    content = Column(Text)
    send_time = Column(DateTime)
    sender_type = Column(String(10))
    chatroom_id = Column(Integer, ForeignKey("chatroom.chatroom_id"))
    chatroom = relationship("Chatroom", back_populates="message")

    __table_args__ = (
        ForeignKeyConstraint(
            ['chatroom_id'], ['chatroom.chatroom_id'],
            name='message_chatroom_id_fkey',
            ondelete="CASCADE"
        ),
    )

class Document(Base):
    __tablename__ = "document"

    document_id = Column(Integer, name="document_id", primary_key=True)
    document_name = Column(String(1000))
    uploaded_name = Column(String(1000))
    uploaded_time = Column(DateTime)
    s3_url = Column(String(1000))
    chatroom_id = Column(Integer, ForeignKey("chatroom.chatroom_id"))
    chatroom = relationship("Chatroom", back_populates="document")

    __table_args__ = (
        ForeignKeyConstraint(
            ['chatroom_id'], ['chatroom.chatroom_id'],
            name='document_chatroom_id_fkey',
            ondelete="CASCADE"
        ),
    )

class EmailVerification(Base):
    __tablename__ = "email_verification"

    email_verification_id = Column(Integer, name="email_verification_id", primary_key=True)
    verifying_email = Column(String(100), nullable=False)
    verification_code = Column(String(5), nullable=False)
    expires_at = Column(DateTime, nullable=False)
    is_verified = Column(Boolean, nullable=False, default=False)

# class Quiz(Base):
#     __tablename__ = "quiz"
#
#     quiz_id = Column(Integer, name="quiz_id", primary_key=True)
#     # session_id = Column() Foreign key