# 국회의원 발의 법안 정보를 외부 국회 API에서 조회하는 라우터
 
import requests # 외부 HTTP 요청을 보내기 위한 라이브러리
import xml.etree.ElementTree as ET # XML 파싱용 라이브러리
from fastapi import APIRouter # 라우터 생성
from fastapi.responses import JSONResponse # 커스텀 JSON 응답 반환용
import os # 환경변수 불러오기용

router = APIRouter()

API_KEY = os.getenv("NA_OPEN_API_KEY") # 국회 API 키를 환경변수에서 불러옴

# 특정 BILL_ID에 해당하는 발의 법안 정보를 외부 국회 API로부터 불러옴
@router.get("/proposed/{bill_id}")
def get_proposed_bill(bill_id: str):
    url = "https://open.assembly.go.kr/portal/openapi/nzmimeepezxkubdpn"
    params = {
        "KEY": API_KEY, # 인증 키
        "Type": "XML", # 응답 형식
        "BILL_ID": bill_id # 조회할 법안 ID
    }

    response = requests.get(url, params=params) # API 요청

    if response.status_code != 200:
        return JSONResponse(content={"error": "국회의원 발의 API 요청 실패"}, status_code=500)

    root = ET.fromstring(response.text) # XML 파싱
    row = root.find("row") # 첫 번째 <row> 태그 찾기

    if row is None:
        return JSONResponse(content={"error": "해당 법안을 찾을 수 없습니다"}, status_code=404)

    # API 결과에서 필요한 항목만 추출하여 JSON 형태로 반환
    result = {
        "bill_id": row.findtext("BILL_ID"),
        "bill_no": row.findtext("BILL_NO"),
        "bill_name": row.findtext("BILL_NAME"),
        "committee": row.findtext("COMMITTEE"),
        "proposer": row.findtext("PROPOSER"),
        "propose_dt": row.findtext("PROPOSE_DT"),
        "proc_resul": row.findtext("PROC_RESUL"),
        "law_proc_r": row.findtext("LAW_PROC_R"),
        "proc_dt": row.findtext("PROC_DT")
    }

    return result
