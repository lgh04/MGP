from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..models.bill import Bill
from ..db import get_db
from sqlalchemy import desc
from app.services import law_api

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



router = APIRouter(prefix="/law", tags=["법률"])

@router.get("/proposals")
def get_proposals():
    return law_api.fetch_law_proposals()

@router.get("/details")
def get_details():
    return law_api.fetch_law_details()


"""
/routers/search.py  
역할:  
법안 검색 및 외부 API를 통해 법안 제안·상세 데이터를 불러오는 API 라우터.  
제목 기반 검색, 상태 필터링, 정렬 방식 설정 기능을 제공하고, 외부 API로부터 입법 관련 데이터를 가져온다.  

연결된 서비스:  
law_api.py: 외부 열린국회 API와 연결되어 법안 제안 목록과 상세 정보를 불러오는 로직이 구현된 서비스 레이어  
models/bill.py: 검색 대상인 법안 데이터 모델 정의  
db/get_db.py: SQLAlchemy 세션 의존성 주입  

엔드포인트 목록:  
법안 검색 = 메서드-GET, 경로-/search, 요청 쿼리 파라미터-title(str), status(str), sort_by(str), 응답-검색된 법안 리스트  
법안 제안 목록 조회 = 메서드-GET, 경로-/law/proposals, 응답-외부 API에서 받아온 법안 제안 데이터  
법안 상세 목록 조회 = 메서드-GET, 경로-/law/details, 응답-외부 API에서 받아온 법안 상세 데이터  

동작 흐름 요약  
/search: 제목을 기준으로 법안을 검색하고, 상태(`draft`, `enacted`)나 정렬 기준(`created_at`, `views`)을 설정해 결과를 필터링한 뒤 번호를 붙여 반환한다.  
/law/proposals: 열린국회 API로부터 법안 제안 목록을 받아와 반환한다.  
/law/details: 열린국회 API로부터 법안 상세 목록을 받아와 반환한다.  
"""
