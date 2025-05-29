from pydantic import BaseModel

class LawDetail(BaseModel):
    bill_id: str
    bill_no: str
    bill_name: str
    committee: str
    propose_dt: str
    proc_result: str
    proposer: str
    law_proc_result: str
    proc_dt: str