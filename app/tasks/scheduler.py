from apscheduler.schedulers.background import BackgroundScheduler # 백그라운드 스케줄러 생성용
from app.db import SessionLocal # DB 세션 팩토리
from app.services.bill_fetcher import save_bills_to_db # 법안 저장 함수

# 스케줄러 시작 함수 (main.py에서 호출됨)
def start_scheduler():
    scheduler = BackgroundScheduler(timezone="Asia/Seoul") # 한국 시간 기준 스케줄러 설정

    # 수행할 작업 정의 (법안 정보를 DB에 저장)
    def task():
        db = SessionLocal() # DB 세션 열기
        try:
            save_bills_to_db(db) # 국회 API에서 가져와 DB에 저장
        finally:
            db.close() # 작업 후 세션 닫기

    # 작업을 매일 새벽 3시에 실행하도록 예약
    scheduler.add_job(task, "cron", hour=3, minute=0)
    scheduler.start() # 스케줄러 시작
