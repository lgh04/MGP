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

"""
/services/bill_fetcher.py
역할:
국회 오픈 API를 통해 법안 데이터를 가져오고, 이를 데이터베이스에 저장하는 역할을 담당하는 서비스 레이어

주요 기능:
-국회 API 요청을 통해 JSON 형식의 법안 데이터 수집
-법안 제목으로 조건 검색 가능 (선택적)
-이미 존재하는 법안은 중복 저장 방지
-새로운 법안 데이터를 SQLAlchemy를 통해 DB에 저장

함수 목록 및 설명:
-def fetch_api_data(url, bill_name=None): 지정된 URL에서 API 데이터를 요청해 JSON 결과를 반환. bill_name 인자를 통해 제목 검색 가능
-def save_bills_to_db(db): 국회 API에서 모든 법안 데이터를 가져와 중복 확인 후 새로운 법안만 DB에 저장

동작 흐름 요약
save_bills_to_db 함수는 URL_2에서 전체 법안 목록을 가져옴
→ 각 법안의 BILL_ID를 기준으로 DB에 존재 여부 확인
→ 존재하지 않는 법안만 SQLAlchemy 모델로 변환 후 DB에 추가
→ 마지막에 전체 커밋하여 저장 완료
"""
