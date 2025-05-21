# 국회 열린API를 통해 법안 목록을 불러오고, 중복되지 않는 새 법안을 데이터베이스에 저장하는 서비스 파일

import requests # HTTP 요청을 보내기 위한 requests 모듈
from sqlalchemy.orm import Session # SQLAlchemy 세션 (DB 작업용)
from app.models.bill import Bill # 법안 테이블 모델

API_KEY = "4fbf8cf2552c4074ac220162a6f1731c" # API 인증키 (공공데이터 포털에서 발급받은 키)

# 국회 API URL (1: 법률안 기본정보, 2: 법률안 심사정보 등)
URL_1 = "https://open.assembly.go.kr/portal/openapi/nzmimeepazxkubdpn"
URL_2 = "https://open.assembly.go.kr/portal/openapi/TVBPMBILL11"

# API에서 법안 데이터 요청
def fetch_api_data(url: str, bill_name: str = None):
    params = {
        "KEY": API_KEY, # API 키
        "Type": "json", # 응답 형식
        "pIndex": 1, # 페이지 번호
        "pSize": 100 # 페이지 크기
    } 
    
    # 특정 법안명 검색 시 파라미터 추가
    if bill_name:
        params["BILL_NAME"] = bill_name
        
    # API 요청 전송
    response = requests.get(url, params=params)
    # 응답 실패 시 빈 리스트 반환
    if response.status_code != 200:
        return []
        
    # 응답 데이터를 JSON으로 파싱
    data = response.json()

    # 데이터 구조에 따라 항목 추출
    items = data.get("nzmimeepazxkubdpn", []) if "nzmimeepazxkubdpn" in data else data.get("TVBPMBILL11", [])
    
    # 2번째 인덱스부터 실제 데이터가 존재 → 존재 시 반환, 없으면 빈 리스트
    return items[1] if len(items) > 1 else []

# API에서 불러온 법안 데이터를 DB에 저장
def save_bills_to_db(db: Session):
    bills = fetch_api_data(URL_2) # URL_2는 법안 심사정보용 API
    for item in bills:
         # 이미 존재하는 BILL_ID는 저장하지 않음 (중복 방지)
        if db.query(Bill).filter(Bill.bill_id == item["BILL_ID"]).first():
            continue

        # 새 법안 객체 생성
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
        # DB에 추가 (아직 커밋은 안 함)
        db.add(bill)
    # 전체 커밋 → 실제로 저장
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
