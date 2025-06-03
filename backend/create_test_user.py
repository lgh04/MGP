from backend.db.database import SessionLocal
from backend.db.models import User
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_test_user():
    db = SessionLocal()
    try:
        # 기존 테스트 사용자가 있는지 확인
        test_user = db.query(User).filter(User.email == "test@example.com").first()
        if test_user:
            print("Test user already exists")
            return
        
        # 새 테스트 사용자 생성
        hashed_password = pwd_context.hash("testpassword")
        test_user = User(
            email="test@example.com",
            name="Test User",
            nickname="testuser",
            hashed_password=hashed_password
        )
        
        db.add(test_user)
        db.commit()
        print("Test user created successfully")
        
    except Exception as e:
        print(f"Error creating test user: {str(e)}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_test_user() 