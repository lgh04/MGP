# 매일 새벽 3시에 국회 API로부터 최신 법안 데이터를 가져와 DB에 저장하는 백그라운드 스케줄러 설정 파일

from apscheduler.schedulers.background import BackgroundScheduler # 백그라운드에서 주기적으로 작업을 실행하기 위한 스케줄러
from app.db import SessionLocal # DB 세션 객체를 생성하기 위한 팩토리 함수
from app.services.bill_fetcher import save_bills_to_db # 국회 API에서 법안 목록을 가져와 DB에 저장하는 함수

# 스케줄러를 시작하는 함수 (main.py 등에서 호출됨)
def start_scheduler():
    scheduler = BackgroundScheduler(timezone="Asia/Seoul") # 한국 시간 기준으로 동작하는 스케줄러 인스턴스 생성

   # 실제로 주기적으로 실행할 작업 정의
    def task():
        db = SessionLocal() # DB 세션 열기
        try:
            save_bills_to_db(db)# 국회 API에서 법안 데이터 가져와 DB에 저장
        finally:
            db.close() # DB 세션 닫기 (리소스 해제)

    # 작업을 매일 새벽 3시에 실행하도록 예약
    scheduler.add_job(task, "cron", hour=3, minute=0)
    scheduler.start() # 스케줄러 시작




"""
/tasks/scheduler.py  
역할:  
APScheduler를 이용해 특정 작업을 매일 새벽 3시에 자동 실행하는 스케줄링 모듈.  

주요 기능:  
-새벽 3시에 국회 API 데이터를 가져와 DB에 저장하는 작업 예약  
-DB 세션을 안전하게 열고 닫으며 작업 수행  

함수 목록 및 설명:  
-def start_scheduler():  
- 백그라운드 스케줄러를 생성하고 시간대를 "Asia/Seoul"로 설정  
- 내부 함수 `task()`를 정의하여 `save_bills_to_db()`를 호출하고 작업 후 DB 세션 종료  
- `task()`를 매일 3시 정각에 실행되도록 cron 방식으로 예약  
- 스케줄러를 시작  

동작 흐름 요약:  
앱이 실행될 때  
→ `start_scheduler()` 호출  
→ APScheduler가 새벽 3시에 `task()`를 자동 실행  
→ 국회 API로부터 법안 정보를 받아 DB에 저장  
"""
