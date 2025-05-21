# 매일 새벽 3시에 국회 API로부터 법안 목록과 상세정보를 받아 콘솔에 출력하는 테스트용 스케줄러 파일

from apscheduler.schedulers.background import BackgroundScheduler # 백그라운드에서 반복 작업을 수행하기 위한 스케줄러
from app.services import law_api # 법안 데이터를 외부 API로부터 가져오는 서비스
import time # 시간 확인용 (테스트 시 사용 가능)

# 자동 갱신 작업 함수
def update_law_data():
    print("🕒 법률 데이터 자동 갱신 중...")
    proposals = law_api.fetch_law_proposals() # 국회 API에서 법안 목록 및 상세정보 수집
    details = law_api.fetch_law_details()
   # TODO: 수집된 데이터를 DB에 저장하는 로직 구현 필요

    # 수집 결과를 콘솔에 출력
    print(f"✅ {len(proposals.get('nzmimeepazxkubdpn', []))}건 제안 수집됨")
    print(f"✅ {len(details.get('TVBPMBILL11', []))}건 상세 수집됨")
    
# 스케줄러 시작 함수
def start_scheduler():
    scheduler = BackgroundScheduler(timezone="Asia/Seoul") # 한국 시간 기준으로 백그라운드 스케줄러 생성
    scheduler.add_job(update_law_data, "cron", hour=3, minute=0)  # 매일 새벽 3시에 update_law_data 작업을 실행하도록 예약
    scheduler.start()  # 스케줄러 시작

