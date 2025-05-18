from apscheduler.schedulers.background import BackgroundScheduler
from app.services import law_api
import time

def update_law_data():
    print("🕒 법률 데이터 자동 갱신 중...")
    proposals = law_api.fetch_law_proposals()
    details = law_api.fetch_law_details()
    # TODO: 데이터 저장 처리
    print(f"✅ {len(proposals.get('nzmimeepazxkubdpn', []))}건 제안 수집됨")
    print(f"✅ {len(details.get('TVBPMBILL11', []))}건 상세 수집됨")

def start_scheduler():
    scheduler = BackgroundScheduler(timezone="Asia/Seoul")
    scheduler.add_job(update_law_data, "cron", hour=3, minute=0)
    scheduler.start()

