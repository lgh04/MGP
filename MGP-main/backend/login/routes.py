from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
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
        print(f"Attempting login for user: {form_data.username}")
        user = authenticate_user(db, form_data.username, form_data.password)
        print(f"Authentication result: {user}")
        
        if not user:
            print("Authentication failed")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="이메일 또는 비밀번호가 올바르지 않습니다.",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        print("Creating access token")
        access_token = create_access_token(
            data={"sub": user.email}
        )
        print("Access token created successfully")
    
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "expires_in": ACCESS_TOKEN_EXPIRE_DAYS * 24 * 60 * 60,
            "user": {
                "email": user.email,
                "name": user.name,
                "nickname": user.nickname
            }
        }
    except Exception as e:
        print(f"Login error: {str(e)}")
        import traceback
        print(f"Full error traceback: {traceback.format_exc()}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"로그인 처리 중 오류가 발생했습니다: {str(e)}"
        )