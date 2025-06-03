from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.sql import func
from database import Base

class Report(Base):
    __tablename__ = "reports"

    id = Column(Integer, primary_key=True, index=True)
    reported_user_id = Column(Integer, ForeignKey("users.id"))
    reporter_id = Column(Integer, ForeignKey("users.id"))
    message_id = Column(Integer, ForeignKey("messages.id"))
    discussion_id = Column(Integer, ForeignKey("discussions.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class UserReportStatus(Base):
    __tablename__ = "user_report_status"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    discussion_id = Column(Integer, ForeignKey("discussions.id"))
    report_count = Column(Integer, default=0)
    is_restricted = Column(Boolean, default=False)
    restriction_start = Column(DateTime(timezone=True), nullable=True)
    restriction_end = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now()) 