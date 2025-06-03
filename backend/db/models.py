from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = "users"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    name = Column(String)
    phone = Column(String)
    nickname = Column(String, unique=True, index=True)
    hashed_password = Column(String)

    votes = relationship("Vote", back_populates="user")
    comments = relationship("Comment", back_populates="user")

    class Config:
        from_attributes = True

class Vote(Base):
    __tablename__ = "votes"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    bill_id = Column(String, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    vote_type = Column(String)  # 'agree' 또는 'disagree'
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="votes")

    class Config:
        from_attributes = True

class Comment(Base):
    __tablename__ = "comments"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    bill_id = Column(String, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    content = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    user = relationship("User", back_populates="comments")

    class Config:
        from_attributes = True 