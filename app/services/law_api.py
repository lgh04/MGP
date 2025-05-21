# 국회 열린 API로부터 법안 목록과 상세 심사정보를 JSON 형식으로 요청·반환하는 외부 데이터 수집 서비스 파일

import requests # 외부 API 요청을 위한 requests 모듈

API_KEY = "4fbf8cf2552c4074ac220162a6f1731c" # 공공데이터 포털에서 발급받은 인증키
HEADERS = {"Content-Type": "application/json"} # 요청 헤더 (JSON 형식 명시)

# 법안 목록을 가져오는 함수
def fetch_law_proposals(p_index=1, p_size=100):
    url = "https://open.assembly.go.kr/portal/openapi/nzmimeepazxkubdpn"
    params = {
        "KEY": API_KEY, # 인증 키
        "Type": "json", # 응답 형식
        "pIndex": p_index, # 페이지 인덱스
        "pSize": p_size, # 페이지당 항목 수
    }
    # API 요청 전송
    response = requests.get(url, params=params, headers=HEADERS)
    return response.json() # JSON 응답 반환

# 법안 상세 심사정보를 가져오는 함수
def fetch_law_details(p_index=1, p_size=100):
    url = "https://open.assembly.go.kr/portal/openapi/TVBPMBILL11" # 심사정보 API URL
    params = {
        "KEY": API_KEY, # 인증 키
        "Type": "json", # 응답 형식
        "pIndex": p_index, # 페이지 인덱스
        "pSize": p_size, # 페이지당 항목 수
    }
    
    # API 요청 전송
    response = requests.get(url, params=params, headers=HEADERS)
    return response.json() # JSON 응답 반환
 

"""
/services/law_api.py  
역할:  
국회의 오픈 API를 통해 법안 목록 및 상세 정보를 요청하고 응답 데이터를 반환하는 서비스 레이어.  

주요 기능:  
-법안 목록(발의 법안) 조회 요청  
-법안 상세 정보 조회 요청  

함수 목록 및 설명:  
-def fetch_law_proposals(p_index=1, p_size=100):  
- 국회 API에서 발의된 법안 목록 데이터를 JSON 형식으로 가져와 반환  
- 인덱스와 페이지 크기를 인자로 받음  

-def fetch_law_details(p_index=1, p_size=100):  
- 국회 API에서 법안의 상세 정보를 JSON 형식으로 가져와 반환  
- 인덱스와 페이지 크기를 인자로 받음  

동작 흐름 요약:  
각 함수는 `requests.get`을 통해 국회 API에 요청을 보내고,  
→ 받은 응답을 `.json()`으로 변환해 반환  
→ 요청 시 API 키와 JSON 응답 형식을 포함한 파라미터를 함께 전달  
"""
