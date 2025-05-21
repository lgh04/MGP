# 최근 등록된 '발의 중' 및 '처리 완료' 법안 각각 최대 7개씩 요약해서 제공하는 API 라우터

from fastapi import APIRouter, Depends # FastAPI 라우터 및 의존성 주입 기능
from sqlalchemy.orm import Session # SQLAlchemy 세션 클래스
from sqlalchemy import desc # 내림차순 정렬을 위한 SQLAlchemy 함수
from ..models.bill import Bill # Bill 테이블 모델 불러오기
from ..db import get_db # DB 세션 생성 함수

# 이 파일의 API들을 묶는 라우터 인스턴스 생성
router = APIRouter()

# 법안 요약 정보 제공 API
@router.get("/summary") # /summary 경로로 GET 요청 시 실행
def get_bill_summary(db: Session = Depends(get_db)):
    result = {} # 결과를 담을 딕셔너리

    # 'draft'와 'enacted' 상태별로 각각 처리
    for status in ["draft", "enacted"]:
        # 해당 상태의 법안을 최신순으로 최대 7개 조회
        bills = (
            db.query(Bill)
            .filter(Bill.status == status)
            .order_by(desc(Bill.created_at)) # 최신순 정렬
            .limit(7) # 최대 7개까지
            .all()
        )

        # 결과 요약 형태로 저장
        result[status] = [
            {
                "name": bill.name, # 법안 이름
                "description": bill.description, # 간단한 설명
                "created_at": bill.created_at # 등록일
            }
            for bill in bills
        ]

    # 전체 결과 반환
    return result



"""
/routers/summary.py  
역할:  
최신 법안 요약 정보를 상태별로 제공하는 API 라우터.  
'발의(draft)'와 '공포(enacted)' 상태의 법안을 각각 최대 7개까지 요약해 반환한다.  

연결된 서비스:  
models/bill.py: 법안 데이터 모델 정의  
db/get_db.py: SQLAlchemy 세션 의존성 주입  

엔드포인트 목록:  
법안 요약 조회 = 메서드-GET, 경로-/summary, 응답-각 상태별로 최신 7개의 법안 요약 데이터 (name, description, created_at 포함)  

동작 흐름 요약  
/summary: 데이터베이스에서 'draft'와 'enacted' 상태의 법안을 각각 생성일 기준으로 정렬해 7개씩 가져와 요약 정보를 반환한다.  
"""
