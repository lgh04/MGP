# 법안 제목과 상태로 검색하고 정렬하며, 외부 API로부터 법안 목록과 상세 정보를 가져오는 복합 검색/조회용 라우터

from fastapi import APIRouter, Depends, HTTPException # FastAPI 관련 기능들 불러오기
from sqlalchemy.orm import Session # SQLAlchemy 세션
from ..models.bill import Bill # Bill 모델 (법안 테이블)
from ..db import get_db # DB 세션 종속성
from sqlalchemy import desc # 정렬을 위한 SQLAlchemy 함수
from app.services import law_api # 외부 API를 통해 법안 정보를 가져오는 서비스

# 라우터 인스턴스 생성 (기본 검색 기능용)
router = APIRouter()

# 법안 검색 API
@router.get("/search") # /search 경로로 GET 요청
def search_bills(
    title: str = "", # 제목 키워드 검색
    status: str = "", # 상태 필터링: "draft" 또는 "enacted"
    sort_by: str = "created_at",  # 기본적으로 created_at 기준으로 정렬 # 정렬 기준: 생성일 or 조회수
    db: Session = Depends(get_db) # DB 세션 주입
):
    # status 값이 유효하지 않으면 예외 처리
    if status and status not in ["draft", "enacted"]:
        raise HTTPException(status_code=400, detail="Invalid status")

     # 제목 기준으로 법안 필터링
    query = db.query(Bill).filter(Bill.name.contains(title))

     # 상태 기준으로 추가 필터링
    if status:
        query = query.filter(Bill.status == status)

     # 정렬 조건 처리
    if sort_by == "created_at":
        query = query.order_by(desc(Bill.created_at))  # 최신순 정렬
    elif sort_by == "views":
        query = query.order_by(desc(Bill.views))  # 조회수 높은 순으로 정렬
    else:
        raise HTTPException(status_code=400, detail="Invalid sort_by value")

    # 쿼리 실행 후 결과 목록 가져오기
    bills = query.all()

    # 각 결과에 인덱스 번호 부여 (프론트에서 표기용)
    for index, bill in enumerate(bills, start=1):
        bill.id = index  # 주의: 실제 id가 아닌 표시용 번호

    # 결과 반환
    return {"bills": bills}


# "/law" 경로를 prefix로 가지는 라우터 인스턴스 생성
router = APIRouter(prefix="/law", tags=["법률"])

# 법안 목록 조회 API (외부 API로부터)
@router.get("/proposals") # /law/proposals 경로로 GET 요청 시 실행
def get_proposals():
    # 외부 API에서 법안 목록 가져와서 반환
    return law_api.fetch_law_proposals()

# 법안 상세 정보 조회 API (외부 API로부터)
@router.get("/details") # /law/details 경로로 GET 요청 시 실행
def get_details():
    # 외부 API에서 법안 상세 정보 가져와서 반환
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
