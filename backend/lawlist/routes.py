# backend/lawlist/routes.py

from fastapi import APIRouter
from typing import Literal
from backend.lawlist.service import search, filter_by_type, sort_data, paginate

router = APIRouter()

@router.get("/law-list")
def get_laws(
    query: str = "",
    mode: Literal["공포", "발의"] = "발의",
    sort: Literal["latest", "views"] = "latest",
    page: int = 1
):
    # 1. 전체 법안 + 검색어 필터링
    all_data = search(query)

    # 2. 공포/발의 구분
    filtered = filter_by_type(all_data, mode)

    # 3. 정렬
    sorted_data = sort_data(filtered, sort)

    # 4. 페이지 나누기
    paged_items, total_pages = paginate(sorted_data, page, size=7)

    # 5. JSON 반환
    return {
        "items": paged_items,
        "total_pages": total_pages,
        "current_page": page
    }
