from fastapi import FastAPI
from .routers import auth, laws, chat, comment, mypage, percent, vote, votecheck, search, summary

app = FastAPI()

# 라우터 등록
app.include_router(auth.router)
app.include_router(laws.router)
app.include_router(search.router, prefix="/bills", tags=["bills"])
app.include_router(summary.router, prefix="/bills", tags=["summary"])
app.include_router(chat.router)
app.include_router(comment.router)
app.include_router(mypage.router)
app.include_router(percent.router)
app.include_router(vote.router)
app.include_router(votecheck.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the ACT:ON API"}
