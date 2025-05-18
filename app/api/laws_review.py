# 특정 법안의 심사 및 처리 결과 정보를 외부 국회 API에서 조회하는 라우터

import requests # 외부 API 요청용
import xml.etree.ElementTree as ET # XML 파싱용
from fastapi import APIRouter # FastAPI 라우터
from fastapi.responses import JSONResponse # JSON 응답 반환용
import os # 환경변수 접근용

router = APIRouter()

API_KEY = os.getenv("NA_OPEN_API_KEY")  # 국회 API 키 (보통 .env에 저장)

# 법안의 심사 및 본회의 처리 결과를 국회 API에서 불러오는 엔드포인트
@router.get("/review/{bill_id}")
def get_bill_review(bill_id: str):
    url = "https://open.assembly.go.kr/portal/openapi/TVBPMBILL11" # 국회 API (법안 심사 정보)
    params = {
        "KEY": API_KEY, # 인증 키
        "Type": "XML", # 응답 타입
        "BILL_ID": bill_id # 법안 ID
    }

    response = requests.get(url, params=params) # API 호출

    if response.status_code != 200:
        return JSONResponse(content={"error": "법안 심사 API 요청 실패"}, status_code=500)

    root = ET.fromstring(response.text) # XML 응답 파싱
    row = root.find("row") # 첫 번째 row 찾기

    if row is None:
        return JSONResponse(content={"error": "법안 정보를 찾을 수 없습니다"}, status_code=404)

    # 필요한 항목만 추출해서 JSON으로 반환
    result = {
        "bill_id": row.findtext("BILL_ID"),
        "bill_no": row.findtext("BILL_NO"),
        "bill_name": row.findtext("BILL_NAME"),
        "proposer": row.findtext("PROPOSER"),
        "propose_dt": row.findtext("PROPOSE_DT"),
        "link_url": row.findtext("LINK_URL"),
        "proc_resul": row.findtext("PROC_RESUL"),
        "proc_dt": row.findtext("PROC_DT")
    }

    return result
