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
