# 'draft'와 'enacted' 상태별로 최근 등록된 법안 7개씩 요약 정보를 반환하는 라우터

from fastapi import APIRouter, Depends # 라우터와 의존성 주입용
from sqlalchemy.orm import Session # DB 세션 타입
from sqlalchemy import desc # 내림차순 정렬용
from ..models.bill import Bill # 법안 모델
from ..db import get_db # DB 세션 생성 함수

# 법안 상태(draft, enacted)별로 최근 등록된 7개의 법안 요약 정보를 제공
router = APIRouter()

@router.get("/summary")
def get_bill_summary(db: Session = Depends(get_db)):
    result = {}

    for status in ["draft", "enacted"]: # 두 가지 상태별로 나눠서 조회
        bills = (
            db.query(Bill)
            .filter(Bill.status == status) # 상태 필터
            .order_by(desc(Bill.created_at)) # 최신순 정렬
            .limit(7) # 최대 7개까지 제한
            .all()
        )

        # 각 상태별 요약 정보 리스트 생성
        result[status] = [
            {
                "name": bill.name, # 법안 이름
                "description": bill.description, # 법안 설명
                "created_at": bill.created_at # 생성일
            }
            for bill in bills
        ]

    # {"draft": [...], "enacted": [...]} 형태로 반환
    return result
