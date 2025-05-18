from sqlalchemy import Column, Integer, String, DateTime, Text, func
from datetime import datetime
from ..db import Base

class Bill(Base):
    __tablename__ = "bills"

    #id = Column(Integer, primary_key=True, index=True)
    #name = Column(String, index=True)
    #description = Column(Text)
    #status = Column(String, index=True)  # 'draft' or 'enacted'
   # created_at = Column(DateTime, default=datetime.utcnow)
   # views = Column(Integer, default=0)

    id = Column(Integer, primary_key=True, index=True)
    bill_id = Column(String, unique=True, index=True)  # BILL_ID
    bill_name = Column(String)  # BILL_NAME
    proposer = Column(String)  # PROPOSER
    committee = Column(String)  # COMMITTEE
    propose_date = Column(String)  # PROPOSE_DT
    proc_result = Column(String)  # PROC_RESULT
    proc_stage = Column(String)  # PROC_STAGE
    law_num = Column(String)  # LAW_NUM
    summary = Column(Text)  # SUMMARY
    created_at = Column(DateTime(timezone=True), server_default=func.now()) 