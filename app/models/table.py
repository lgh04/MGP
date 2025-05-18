#모델(Bill 등)을 기반으로 데이터베이스에 테이블을 생성하는 초기화 스크립트

from db import Base, engine # Base는 모든 모델들의 부모 클래스, engine은 DB 연결 객체
from models.bill import Bill # Bill 모델을 가져와야 테이블 생성 대상에 포함됨

# Base를 상속한 모든 모델(Bill 등)을 기준으로 실제 DB에 테이블 생성
# 이미 테이블이 존재하면 무시되고, 없을 때만 생성됨
Base.metadata.create_all(bind=engine)
