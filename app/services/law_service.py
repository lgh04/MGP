import requests

def fetch_law_detail(law_id: str) -> dict:
    try:
        url = f"https://open.assembly.go.kr/portal/openapi/nzmimeepazxkubdpn"  # 예시용 API 키
        params = {
            'KEY': 'YOUR_API_KEY_HERE',  # 실제 발급받은 API 키
            'Type': 'json',
            'AGE': '21',
            'BILL_ID': law_id
        }
        response = requests.get(url, params=params)
        if response.status_code == 200:
            result = response.json()
            bill_data = result['nzmimeepazxkubdpn'][1]['row'][0]  # 실제 응답 구조에 따라 조정
            return {
                "title": bill_data.get("BILL_NAME", "제목 없음"),
                "content": bill_data.get("RST_PROPOSER", "내용 없음")  # 설명이 들어있는 다른 필드를 사용할 수도 있음
            }
        else:
            return {"title": "법안 정보를 불러오지 못했습니다", "content": ""}
    except Exception as e:
        print("API 호출 오류:", e)
        return {"title": "API 오류 발생", "content": ""}


"""
/services/law_service.py  
역할:  
특정 법안 ID에 대한 상세 정보를 국회 API에서 조회하여 필요한 정보를 가공해 반환하는 서비스 레이어.  

주요 기능:  
-법안 ID를 기반으로 법안 상세 정보 조회  
-응답 데이터 중 필요한 필드만 추출해 가공된 딕셔너리 형태로 반환  

함수 목록 및 설명:  
-def fetch_law_detail(law_id: str) -> dict:  
- 국회 API에 BILL_ID를 전달해 해당 법안의 상세 데이터를 요청  
- 응답이 성공적일 경우 제목(`BILL_NAME`)과 제안자(`RST_PROPOSER`) 정보를 딕셔너리로 구성해 반환  
- 실패 시 에러 메시지와 함께 기본 응답 반환  
- 예외 발생 시 콘솔 출력 및 오류 메시지 반환  

동작 흐름 요약:  
법안 ID를 파라미터로 받아  
→ 국회 API에 요청  
→ 응답에서 `BILL_NAME`과 `RST_PROPOSER`를 추출  
→ 이를 `"title"`과 `"content"` 필드로 반환  
→ 실패 시 오류 메시지를 포함한 기본 구조 반환  
"""
