# 법안 제목 검색, 상태 필터링, 정렬 기능을 제공하는 법안 검색 API 라우터

from fastapi import APIRouter, Depends, HTTPException # 라우터 및 예외처리, 의존성 주입
from sqlalchemy.orm import Session # DB 세션 타입
from ..models.bill import Bill # 법안 모델
from ..db import get_db # DB 세션 주입 함수
from sqlalchemy import desc # 내림차순 정렬용

# 법안 제목 검색 + 상태 필터 + 정렬 옵션 제공
router = APIRouter()

@router.get("/search")
def search_bills(
    title: str = "", # 검색할 법안 제목 (포함 검색)
    status: str = "", # 상태 필터 ("draft" 또는 "enacted")
    sort_by: str = "created_at", # 정렬 기준 ("created_at", "views")
    db: Session = Depends(get_db) # DB 세션 주입
):
    # 상태 필터 값이 유효한지 확인
    if status and status not in ["draft", "enacted"]:
        raise HTTPException(status_code=400, detail="Invalid status")

    # 제목 포함 검색 쿼리 시작
    query = db.query(Bill).filter(Bill.name.contains(title))

    # 상태 필터가 있다면 추가
    if status:
        query = query.filter(Bill.status == status)

    # 정렬 기준 처리 (created_at: 최신순, views: 조회수순)
    if sort_by == "created_at":
        query = query.order_by(desc(Bill.created_at))  # 최신순 정렬
    elif sort_by == "views":
        query = query.order_by(desc(Bill.views))  # 조회수 높은 순으로 정렬
    else:
        raise HTTPException(status_code=400, detail="Invalid sort_by value")

    # 최종 결과 쿼리 실행
    bills = query.all()

    # 검색 결과에 번호 붙이기 (1부터 시작)
    for index, bill in enumerate(bills, start=1):
        bill.id = index  # 실제 DB ID를 덮어쓸 수 있어 주의 필요
        
    return {"bills": bills} # 결과 반환
