from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from backend.db.database import get_db
from .crud import authenticate_user
from backend.user.auth import create_access_token, ACCESS_TOKEN_EXPIRE_DAYS
from fastapi.middleware.cors import CORSMiddleware

router = APIRouter(
    prefix="/api",
    tags=["login"]
)

@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    try:
        print(f"Login attempt with username: {form_data.username}")
        # 사용자 인증
        user = authenticate_user(db, form_data.username, form_data.password)
        if not user:
<<<<<<< Updated upstream
            print("Authentication failed")
            return JSONResponse(
=======
            raise HTTPException(
>>>>>>> Stashed changes
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": "이메일 또는 비밀번호가 올바르지 않습니다."},
                headers={"WWW-Authenticate": "Bearer"}
            )
<<<<<<< Updated upstream
        
        print(f"Authentication successful, creating access token for user: {user.email}")
        # 액세스 토큰 생성
        access_token = create_access_token(
            data={"sub": user.email}
        )
        
        # 응답 반환
        response_data = {
=======
        access_token = create_access_token(
            data={"sub": user.email}
        )
        return {
>>>>>>> Stashed changes
            "access_token": access_token,
            "token_type": "bearer",
            "expires_in": ACCESS_TOKEN_EXPIRE_DAYS * 24 * 60 * 60,
            "user": {
                "email": user.email,
                "name": user.name,
                "nickname": user.nickname
            }
        }
        
        return JSONResponse(
            content=response_data,
            headers={
                "Access-Control-Allow-Credentials": "true",
                "Access-Control-Allow-Origin": "http://localhost:3000"
            }
        )
        
    except Exception as e:
        print(f"Login error: {str(e)}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": "로그인 처리 중 오류가 발생했습니다."}
        )