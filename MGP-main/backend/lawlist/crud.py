# backend/lawlist/crud.py

import requests
import time
import traceback

API_KEY = "590f3e7eaec4451699d6828cf5ba47f2"
_cached_data = None

def fetch_all_laws():
    global _cached_data
    if _cached_data is not None:
        return _cached_data

    url = "https://open.assembly.go.kr/portal/openapi/TVBPMBILL11"
    pIndex = 1
    page_size = 500
    all_rows = []

    while True:
        params = {
            "KEY": API_KEY,
            "Type": "json",
            "pIndex": pIndex,
            "pSize": page_size,
            "AGE": "22"
        }

        try:
            res = requests.get(url, params=params)
            data = res.json()
            key = list(data.keys())[0]

            if not isinstance(data[key], list) or len(data[key]) < 2 or "row" not in data[key][1]:
                break

            rows = data[key][1]["row"]
            if not rows:
                break

            all_rows.extend(rows)
            pIndex += 1
            time.sleep(0.3)

        except Exception as e:
            print("❌ API 오류 발생:")
            traceback.print_exc()
            break

    result = {"공포": [], "발의": []}
    processed_statuses = ["가결", "부결", "폐기", "철회", "원안가결", "수정가결"]

    for item in all_rows:
        status = (item.get("PROC_RESULT_CD") or "").strip()
        bill_id = item.get("BILL_ID", "")
        link = f"https://likms.assembly.go.kr/bill/billDetail.do?billId={bill_id}" if bill_id else "#"

        entry = {
            "title": item.get("BILL_NAME", "제목 없음"),
            "link": link,
            "date": item.get("PROPOSE_DT", "날짜 없음"),
            "proposer": item.get("PROPOSER", "제안자 없음"),
            "bill_no": item.get("BILL_NO", "의안번호 없음"),
            "committee": item.get("CURR_COMMITTEE", "소관위 없음"),
            "result": item.get("PROC_RESULT_CD", "결과 없음"),
            "bill_id": item.get("BILL_ID", "")
        }

        if status in processed_statuses:
            result["공포"].append(entry)
        else:
            result["발의"].append(entry)

    _cached_data = result
    return result
