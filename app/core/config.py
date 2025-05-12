# app/config.py
import os
from dotenv import load_dotenv

load_dotenv()  # .env 파일에서 환경 변수 로드

DATABASE_URL = os.getenv("DATABASE_URL")
SECRET_KEY = os.getenv("SECRET_KEY, default_secret_key")
