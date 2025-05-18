import requests
from sqlalchemy.orm import Session
from app.models.bill import Bill

API_KEY = "4fbf8cf2552c4074ac220162a6f1731c"
URL_1 = "https://open.assembly.go.kr/portal/openapi/nzmimeepazxkubdpn"
URL_2 = "https://open.assembly.go.kr/portal/openapi/TVBPMBILL11"

def fetch_api_data(url: str, bill_name: str = None):
    params = {
        "KEY": API_KEY,
        "Type": "json",
        "pIndex": 1,
        "pSize": 100
    }
    if bill_name:
        params["BILL_NAME"] = bill_name

    response = requests.get(url, params=params)
    if response.status_code != 200:
        return []

    data = response.json()
    items = data.get("nzmimeepazxkubdpn", []) if "nzmimeepazxkubdpn" in data else data.get("TVBPMBILL11", [])
    return items[1] if len(items) > 1 else []

def save_bills_to_db(db: Session):
    bills = fetch_api_data(URL_2)
    for item in bills:
        if db.query(Bill).filter(Bill.bill_id == item["BILL_ID"]).first():
            continue
        bill = Bill(
            bill_id=item.get("BILL_ID"),
            bill_name=item.get("BILL_NAME"),
            proposer=item.get("PROPOSER"),
            committee=item.get("COMMITTEE"),
            propose_date=item.get("PROPOSE_DT"),
            proc_result=item.get("PROC_RESULT"),
            proc_stage=item.get("PROC_STAGE"),
            law_num=item.get("LAW_NUM"),
            summary=item.get("SUMMARY")
        )
        db.add(bill)
    db.commit()