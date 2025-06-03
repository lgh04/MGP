# backend/lawdetail/crud.py
import requests
import traceback
import logging
import json

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

API_KEY = "590f3e7eaec4451699d6828cf5ba47f2"

def fetch_law_detail(bill_id: str):
    if not bill_id or bill_id == "undefined":
        logger.error(f"잘못된 bill_id가 전달됨: {bill_id}")
        return {"error": "유효하지 않은 법안 ID입니다."}

    url = "https://open.assembly.go.kr/portal/openapi/TVBPMBILL11"
    params = {
        "KEY": API_KEY,
        "Type": "json",
        "BILL_ID": bill_id,
    }

    try:
        logger.info(f"API 요청: {url} - 파라미터: {params}")
        response = requests.get(url, params=params)
        response.raise_for_status()  # HTTP 오류 발생시 예외 발생
        
        logger.info(f"API 응답 상태 코드: {response.status_code}")
        
        try:
            data = response.json()
            logger.info(f"API 응답 데이터: {json.dumps(data, ensure_ascii=False, indent=2)}")
            
            # API 응답 구조 검증
            if not data:
                logger.error("API 응답이 비어있습니다.")
                return {"error": "API 응답이 비어있습니다."}
                
            # TVBPMBILL11 키가 있는지 확인
            if "TVBPMBILL11" not in data:
                logger.error(f"API 응답에 TVBPMBILL11 키가 없습니다. 응답: {data}")
                return {"error": "데이터를 찾을 수 없습니다."}
                
            tvbpm_data = data["TVBPMBILL11"]
            
            # 응답 데이터가 리스트가 아닌 경우 처리
            if not isinstance(tvbpm_data, list):
                logger.error(f"TVBPMBILL11 데이터가 리스트가 아닙니다: {tvbpm_data}")
                return {"error": "잘못된 데이터 형식"}
                
            # 응답 데이터가 비어있는 경우 처리
            if len(tvbpm_data) < 2:
                logger.error(f"TVBPMBILL11 데이터가 비어있습니다: {tvbpm_data}")
                return {"error": "데이터가 비어있습니다"}
                
            # row 데이터 가져오기
            rows = tvbpm_data[1].get("row", [])
            if not rows:
                logger.warning(f"검색된 법안 정보가 없습니다. (bill_id: {bill_id})")
                return {"error": "해당 법안 정보를 찾을 수 없습니다."}
                
            return rows[0]
            
        except json.JSONDecodeError as e:
            logger.error(f"JSON 파싱 실패: {str(e)}\n응답 내용: {response.text}")
            return {"error": "API 응답을 파싱할 수 없습니다."}
            
    except requests.exceptions.HTTPError as e:
        logger.error(f"HTTP 오류 발생: {str(e)}")
        return {"error": f"API 서버 오류: {response.status_code}"}
        
    except requests.exceptions.RequestException as e:
        logger.error(f"API 요청 실패: {str(e)}")
        return {"error": "API 서버에 연결할 수 없습니다."}
        
    except Exception as e:
        logger.error(f"예상치 못한 오류 발생: {str(e)}")
        traceback.print_exc()
        return {"error": "내부 서버 오류가 발생했습니다."}
