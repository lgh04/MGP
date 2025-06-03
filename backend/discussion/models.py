from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from backend.db.database import Base

class Discussion(Base):
    __tablename__ = "discussions"

    id = Column(Integer, primary_key=True, index=True)
    bill_id = Column(String, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    participants = relationship("DiscussionParticipant", back_populates="discussion")
    messages = relationship("DiscussionMessage", back_populates="discussion")

class DiscussionParticipant(Base):
    __tablename__ = "discussion_participants"

    id = Column(Integer, primary_key=True, index=True)
    discussion_id = Column(Integer, ForeignKey("discussions.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    joined_at = Column(DateTime, default=datetime.utcnow)

    discussion = relationship("Discussion", back_populates="participants")
    user = relationship("User")

class DiscussionMessage(Base):
    __tablename__ = "discussion_messages"

    id = Column(Integer, primary_key=True, index=True)
    discussion_id = Column(Integer, ForeignKey("discussions.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    content = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

    discussion = relationship("Discussion", back_populates="messages")
    user = relationship("User") 