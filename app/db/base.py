#Base 클래스 정의 파일

from sqlalchemy.ext.declarative import declarative_base # SQLAlchemy 모델 생성을 위한 기본 클래스 생성 함수

Base = declarative_base() # 모든 모델들이 상속받는 공통 부모 클래스
