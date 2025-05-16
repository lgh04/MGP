from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..models.bill import Bill
from ..db import get_db
from sqlalchemy import desc

router = APIRouter()

@router.get("/search")
def search_bills(
    title: str = "",
    status: str = "",
    sort_by: str = "created_at",  # 기본적으로 created_at 기준으로 정렬
    db: Session = Depends(get_db)
):
    # status가 있으면 유효성 검사
    if status and status not in ["draft", "enacted"]:
        raise HTTPException(status_code=400, detail="Invalid status")

    # 쿼리 준비
    query = db.query(Bill).filter(Bill.name.contains(title))

    # status가 있을 경우 필터 추가
    if status:
        query = query.filter(Bill.status == status)

    # sort_by가 created_at이면 최신순 정렬, views이면 조회수 높은 순으로 정렬
    if sort_by == "created_at":
        query = query.order_by(desc(Bill.created_at))  # 최신순 정렬
    elif sort_by == "views":
        query = query.order_by(desc(Bill.views))  # 조회수 높은 순으로 정렬
    else:
        raise HTTPException(status_code=400, detail="Invalid sort_by value")

    # 검색된 모든 결과를 가져옴
    bills = query.all()

    # 결과에 번호 붙이기
    for index, bill in enumerate(bills, start=1):
        bill.id = index  # 검색된 항목에 번호를 붙여줌 (번호는 1부터 시작)

    return {"bills": bills}
