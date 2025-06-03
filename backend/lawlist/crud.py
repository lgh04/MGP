# backend/lawlist/crud.py

import requests
import time
import traceback
from fastapi import HTTPException

API_KEY = "590f3e7eaec4451699d6828cf5ba47f2"
_cached_data = None
_last_fetch_time = 0
CACHE_DURATION = 3600  # 1시간

def fetch_all_laws():
    global _cached_data, _last_fetch_time
    current_time = time.time()
    
    # 캐시가 있고 1시간이 지나지 않았다면 캐시된 데이터 반환
    if _cached_data is not None and (current_time - _last_fetch_time) < CACHE_DURATION:
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
            print(f"Fetching page {pIndex}...")
            res = requests.get(url, params=params, timeout=10)
            
            if res.status_code != 200:
                print(f"API 응답 오류: {res.status_code}")
                raise HTTPException(status_code=502, detail="국회 API 서버 오류")
            
            data = res.json()
            key = list(data.keys())[0]

            if not isinstance(data[key], list) or len(data[key]) < 2 or "row" not in data[key][1]:
                break

            rows = data[key][1]["row"]
            if not rows:
                break

            all_rows.extend(rows)
            print(f"Page {pIndex} fetched successfully. Total rows: {len(all_rows)}")
            
            pIndex += 1
            time.sleep(0.3)  # API 호출 간격 조절

        except requests.exceptions.Timeout:
            print("API 타임아웃 발생")
            raise HTTPException(status_code=504, detail="국회 API 서버 타임아웃")
        except requests.exceptions.RequestException as e:
            print(f"API 요청 오류: {str(e)}")
            raise HTTPException(status_code=502, detail="국회 API 서버 연결 오류")
        except Exception as e:
            print("❌ API 오류 발생:")
            traceback.print_exc()
            if _cached_data is not None:
                print("캐시된 데이터 반환")
                return _cached_data
            raise HTTPException(status_code=500, detail="법안 데이터 처리 중 오류 발생")

    result = {"공포": [], "발의": []}
    processed_statuses = ["가결", "부결", "폐기", "철회", "원안가결", "수정가결"]

    for item in all_rows:
        try:
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
                "bill_id": bill_id
            }

            if status in processed_statuses:
                result["공포"].append(entry)
            else:
                result["발의"].append(entry)
        except Exception as e:
            print(f"법안 데이터 처리 오류: {str(e)}")
            continue

    _cached_data = result
    _last_fetch_time = current_time
    print(f"데이터 가져오기 완료. 공포: {len(result['공포'])}건, 발의: {len(result['발의'])}건")
    return result
