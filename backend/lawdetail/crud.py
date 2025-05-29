# --- crud.py ---
import requests
import xml.etree.ElementTree as ET

API_KEY = "590f3e7eaec4451699d6828cf5ba47f2"
AGE = 22


def fetch_law_by_bill_no(bill_no: str):
    url = (
        f"https://open.assembly.go.kr/portal/openapi/nzmimeepazxkubdpn"
        f"?KEY={API_KEY}&Type=XML&AGE={AGE}&BILL_NO={bill_no}"
    )

    response = requests.get(url)
    if response.status_code != 200:
        raise Exception("API 요청 실패")

    root = ET.fromstring(response.content)
    row = root.find(".//row")
    if row is None:
        raise Exception("법안 정보를 찾을 수 없음")

    result = {}
    for child in row:
        result[child.tag] = child.text
    return result
