from sqlalchemy import Column, String, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from backend.db.session import Base

class User(Base):
    __tablename__ = "user"

    user_id = Column(Integer, name="user_id", primary_key=True)
    first_name = Column(String(20), nullable=False)
    last_name = Column(String(20), nullable=False)
    email = Column(String(50), unique=True, nullable=False)
    password = Column(String(100), nullable=False)
    chatroom = relationship("Chatroom", back_populates="user")

class Chatroom(Base):
    __tablename__ = "chatroom"

    chatroom_id = Column(Integer, name="chatroom_id", primary_key=True)
    chatroom_name = Column(String(50))
    instructor_name = Column(String(20))
    course_code = Column(String(20))
    user_id = Column(Integer, ForeignKey("user.user_id"), nullable=False)
    user = relationship("User", back_populates="chatroom")
    message = relationship("Message", back_populates="chatroom")
    document = relationship("Document", back_populates="chatroom")


class Message(Base):
    __tablename__ = "message"
    message_id = Column(Integer, primary_key=True)
    content = Column(String(500))
    send_time = Column(DateTime)
    sender_type = Column(String(10))
    chatroom_id = Column(Integer, ForeignKey("chatroom.chatroom_id"), nullable=False)
    chatroom = relationship("Chatroom", back_populates="message")

class Document(Base):
    __tablename__ = "document"

    document_id = Column(Integer, name="document_id", primary_key=True)
    document_name = Column(String(1000))
    uploaded_name = Column(String(1000))
    uploaded_time = Column(DateTime)
    s3_url = Column(String(1000))
    chatroom_id = Column(Integer, ForeignKey("chatroom.chatroom_id"))
    chatroom = relationship("Chatroom", back_populates="document")

# class Quiz(Base):
#     __tablename__ = "quiz"
#
#     quiz_id = Column(Integer, name="quiz_id", primary_key=True)
#     # session_id = Column() Foreign key