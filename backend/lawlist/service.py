# backend/lawlist/service.py

from backend.lawlist.crud import fetch_all_laws
from fastapi import HTTPException

def search(query: str):
    try:
        data = fetch_all_laws()
        if not query:
            return data

        result = {"공포": [], "발의": []}
        for mode in ["공포", "발의"]:
            for item in data[mode]:
                # 제목, 제안자, 의안번호에서 검색
                if (query.lower() in item["title"].lower() or
                    query.lower() in item["proposer"].lower() or
                    query.lower() in item["bill_no"].lower()):
                    result[mode].append(item)
        return result
    except Exception as e:
        print(f"검색 중 오류 발생: {str(e)}")
        raise HTTPException(status_code=500, detail="법안 검색 중 오류가 발생했습니다.")

def filter_by_type(data, mode):
    try:
        return data[mode]
    except KeyError:
        print(f"잘못된 모드: {mode}")
        raise HTTPException(status_code=400, detail="잘못된 검색 모드입니다.")
    except Exception as e:
        print(f"필터링 중 오류 발생: {str(e)}")
        raise HTTPException(status_code=500, detail="법안 필터링 중 오류가 발생했습니다.")

def sort_data(data, 기준):
    try:
        if 기준 == "latest":
            return sorted(data, key=lambda x: x.get("date", ""), reverse=True)
        elif 기준 == "views":
            return sorted(data, key=lambda x: x.get("views", 0), reverse=True)
        return data
    except Exception as e:
        print(f"정렬 중 오류 발생: {str(e)}")
        raise HTTPException(status_code=500, detail="법안 정렬 중 오류가 발생했습니다.")

def paginate(data, page, size=7):
    try:
        if not data:
            return [], 0
            
        total_pages = (len(data) + size - 1) // size
        page = max(1, min(page, total_pages))  # 페이지 범위 제한
        start = (page - 1) * size
        end = start + size
        return data[start:end], total_pages
    except Exception as e:
        print(f"페이지네이션 중 오류 발생: {str(e)}")
        raise HTTPException(status_code=500, detail="페이지네이션 중 오류가 발생했습니다.")
