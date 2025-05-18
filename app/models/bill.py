#법안 정보를 DB에 저장하기 위한 모델 파일 (DB 테이블 구조)

from sqlalchemy import Column, Integer, String, DateTime, Text, func
from datetime import datetime
from ..db import Base # 프로젝트 내에서 선언한 Base 클래스(SQLAlchemy의 declarative_base())

# Bill 클래스는 SQLAlchemy ORM 모델로, 'bills'라는 테이블을 정의함
class Bill(Base):
    __tablename__ = "bills" # 테이블 이름을 'bills'로 지정

    id = Column(Integer, primary_key=True, index=True) # 고유 식별자(PK), 자동 증가됨. 각 법안 레코드를 구분하는 기본 키
    bill_id = Column(String, unique=True, index=True)  # 외부 API 또는 고유 식별용으로 사용되는 법안 ID. 중복되면 안 됨.
    bill_name = Column(String)  # 법안의 제목
    proposer = Column(String)  # 법안을 제안한 사람 (국회의원 이름 등)
    committee = Column(String)  # 담당 위원회 (예: 국토교통위원회, 법제사법위원회 등)
    propose_date = Column(String)  # 법안 제안 날짜 (문자열 형태로 저장됨. 예: '2025-05-18')
    proc_result = Column(String)  # 법안 처리 결과 (예: '본회의 통과', '폐기', '심사중')
    proc_stage = Column(String)  # 현재 처리 단계 (예: 소관위 심사 중, 법사위 계류 등)
    law_num = Column(String)  # 법률 번호 (예: 법률 제12345호)
    summary = Column(Text) # 법안에 대한 설명, 요약된 내용 (길게 작성되므로 Text 타입 사용)
    created_at = Column(DateTime(timezone=True), server_default=func.now()) # 데이터가 DB에 삽입될 때의 시간 자동 저장 (timezone 포함)
