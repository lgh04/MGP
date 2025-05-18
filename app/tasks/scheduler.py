from apscheduler.schedulers.background import BackgroundScheduler
from app.db import SessionLocal
from app.services.bill_fetcher import save_bills_to_db

def start_scheduler():
    scheduler = BackgroundScheduler(timezone="Asia/Seoul")
    
    def task():
        db = SessionLocal()
        try:
            save_bills_to_db(db)
        finally:
            db.close()
    
    scheduler.add_job(task, "cron", hour=3, minute=0)
    scheduler.start()