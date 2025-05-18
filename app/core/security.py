#비밀번호 해싱 및 JWT 액세스 토큰 생성 처리 보안 유틸리티 파일

from passlib.context import CryptContext # 비밀번호 해싱용 라이브러리
from jose import JWTError, jwt# JWT 생성 및 검증 라이브러리
from datetime import datetime, timedelta
from .config import SECRET_KEY # 토큰 암호화에 사용할 비밀키 불러오기

# bcrypt 알고리즘을 사용하는 해싱 설정
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    return pwd_context.hash(password) # 비밀번호를 해시로 변환

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password) # 비밀번호 일치 여부 확인

def create_access_token(data: dict, expires_delta: timedelta = timedelta(hours=1)):
    to_encode = data.copy() # 복사해서 변형
    to_encode.update({"exp": datetime.utcnow() + expires_delta}) # 만료 시간 추가
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm="HS256") # JWT 토큰 생성
    return encoded_jwt # 토큰 반환
