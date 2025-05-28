from sqlalchemy.orm import Session
from ..user.models import User  # ✅ 상대경로로 수정

# ✅ 로그인 시 이메일/비밀번호 검증 함수
def authenticate_user(db: Session, email: str, password: str):
    user = db.query(User).filter(User.email == email).first()
    if user and user.password == password:
        return user
    return None
