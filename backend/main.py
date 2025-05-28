# main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.user.routes import router as user_router
from backend.login.routes import router as login_router
from backend.law.routes import router as law_router
from backend.lawlist.routes import router as lawlist_router
from backend.db.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router, prefix="/users", tags=["user"])
app.include_router(login_router, prefix="/auth", tags=["login"])
app.include_router(law_router, prefix="/api", tags=["law"])
app.include_router(lawlist_router, prefix="/api", tags=["lawlist"])
