from sqlalchemy import Column, Integer, String, DateTime, Text
from datetime import datetime
from ..db import Base

class Bill(Base):
    __tablename__ = "bills"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(Text)
    status = Column(String, index=True)  # 'draft' or 'enacted'
    created_at = Column(DateTime, default=datetime.utcnow)
    views = Column(Integer, default=0)
