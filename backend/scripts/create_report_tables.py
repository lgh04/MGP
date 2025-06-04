from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import sys
import os

# 프로젝트 루트 디렉토리를 파이썬 경로에 추가
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from backend.discussion.models import Discussion
from backend.db.database import engine, SessionLocal

def create_missing_report_tables():
    """기존에 생성된 모든 토론방의 신고 테이블을 생성합니다."""
    db = SessionLocal()
    try:
        # 모든 토론방 조회
        discussions = db.query(Discussion).all()
        print(f"총 {len(discussions)}개의 토론방을 확인합니다.")

        for discussion in discussions:
            try:
                # 신고 테이블 생성 시도
                discussion.create_report_table()
                print(f"토론방 ID {discussion.id}의 신고 테이블 생성 완료")
            except Exception as e:
                print(f"토론방 ID {discussion.id}의 신고 테이블 생성 실패: {str(e)}")
    
    finally:
        db.close()

if __name__ == "__main__":
    print("신고 테이블 생성을 시작합니다...")
    create_missing_report_tables()
    print("신고 테이블 생성이 완료되었습니다.") 