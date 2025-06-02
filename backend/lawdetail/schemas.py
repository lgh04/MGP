# backend/lawdetail/schemas.py
from pydantic import BaseModel
from typing import Optional

class LawDetail(BaseModel):
    BILL_ID: str
    BILL_NO: Optional[str]
    AGE: Optional[str]
    BILL_NAME: Optional[str]
    PROPOSER: Optional[str]
    PROPOSER_KIND: Optional[str]
    PROPOSE_DT: Optional[str]
    CURR_COMMITTEE_ID: Optional[str]
    CURR_COMMITTEE: Optional[str]
    COMMITTEE_DT: Optional[str]
    COMMITTEE_PROC_DT: Optional[str]
    LINK_URL: Optional[str]
    RST_PROPOSER: Optional[str]
    LAW_PROC_RESULT_CD: Optional[str]
    LAW_PROC_DT: Optional[str]
    LAW_PRESENT_DT: Optional[str]
    LAW_SUBMIT_DT: Optional[str]
    CMT_PROC_RESULT_CD: Optional[str]
    CMT_PROC_DT: Optional[str]
    CMT_PRESENT_DT: Optional[str]
    RST_MONA_CD: Optional[str]
    PROC_RESULT_CD: Optional[str]
    PROC_DT: Optional[str]

    class Config:
        from_attributes = True  # Pydantic v2에서는 orm_mode 대신 이걸 써야 함
