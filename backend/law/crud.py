import requests
import time
import traceback

API_KEY = "590f3e7eaec4451699d6828cf5ba47f2"

def fetch_all_laws():
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
            print("오류 메시지:", e)
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
            "date": item.get("PROPOSE_DT", "날짜 없음")
        }

        if status in processed_statuses:
            result["공포"].append(entry)
        else:
            result["발의"].append(entry)

    print(f"✅ 총 {len(result['공포'])}건 처리됨 / {len(result['발의'])}건 계류됨")
    return result
