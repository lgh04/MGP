# backend/lawlist/service.py

from backend.lawlist.crud import fetch_all_laws

def search(query: str):
    data = fetch_all_laws()
    if not query:
        return data

    result = {"공포": [], "발의": []}
    for mode in ["공포", "발의"]:
        for item in data[mode]:
            if query.lower() in item["title"].lower():
                result[mode].append(item)
    return result

def filter_by_type(data, mode):
    return data[mode]

def sort_data(data, 기준):
    if 기준 == "latest":
        return sorted(data, key=lambda x: x["date"], reverse=True)
    elif 기준 == "views":
        return sorted(data, key=lambda x: x.get("views", 0), reverse=True)
    return data

def paginate(data, page, size=7):
    total_pages = (len(data) + size - 1) // size
    start = (page - 1) * size
    end = start + size
    return data[start:end], total_pages
