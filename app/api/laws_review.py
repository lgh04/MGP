import requests
import xml.etree.ElementTree as ET
from fastapi import APIRouter
from fastapi.responses import JSONResponse
import os

router = APIRouter()

API_KEY = os.getenv("NA_OPEN_API_KEY")  # 또는 config에서 import

@router.get("/review/{bill_id}")
def get_bill_review(bill_id: str):
    url = "https://open.assembly.go.kr/portal/openapi/TVBPMBILL11"
    params = {
        "KEY": API_KEY,
        "Type": "XML",
        "BILL_ID": bill_id
    }

    response = requests.get(url, params=params)

    if response.status_code != 200:
        return JSONResponse(content={"error": "법안 심사 API 요청 실패"}, status_code=500)

    root = ET.fromstring(response.text)
    row = root.find("row")

    if row is None:
        return JSONResponse(content={"error": "법안 정보를 찾을 수 없습니다"}, status_code=404)

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