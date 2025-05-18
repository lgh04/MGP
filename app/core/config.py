# app/config.py
# 환경 변수를 불러와 DB 주소와 시크릿 키를 설정하는 설정 파일

import os
from dotenv import load_dotenv # .env 파일 지원을 위한 외부 라이브러리

load_dotenv()  # .env 파일에서 환경 변수 로드

DATABASE_URL = os.getenv("DATABASE_URL") # DB 연결 주소 불러오기
SECRET_KEY = os.getenv("SECRET_KEY", "default_secret_key") #여기 따옴표 확인!!
