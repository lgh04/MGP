from sqlalchemy.orm import Session
from backend.db.models import User  # 절대 경로로 수정
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

# ✅ 로그인 시 이메일/비밀번호 검증 함수
def authenticate_user(db: Session, email: str, password: str):
    try:
        print(f"Attempting to authenticate user with email: {email}")
        user = db.query(User).filter(User.email == email).first()
        if not user:
            print(f"No user found with email: {email}")
            return False
        
        print(f"User found, verifying password...")
        if not verify_password(password, user.hashed_password):
            print(f"Password verification failed for user: {email}")
            return False
        
        print(f"Authentication successful for user: {email}")
        return user
    except Exception as e:
        print(f"Authentication error: {str(e)}")
        return False
