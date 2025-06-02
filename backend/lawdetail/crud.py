# backend/lawdetail/crud.py
import requests
import traceback

API_KEY = "590f3e7eaec4451699d6828cf5ba47f2"

def fetch_law_detail(bill_id: str):
    url = "https://open.assembly.go.kr/portal/openapi/TVBPMBILL11"
    params = {
        "KEY": API_KEY,
        "Type": "json",
        "BILL_ID": bill_id,
    }

    try:
        response = requests.get(url, params=params)
        data = response.json()
        rows = data["TVBPMBILL11"][1].get("row", [])
        return rows[0] if rows else None
    except Exception:
        traceback.print_exc()
        return None
