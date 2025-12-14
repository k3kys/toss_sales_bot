# app/main.py
from fastapi import FastAPI, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from contextlib import asynccontextmanager
from sqlalchemy.orm import Session # DB 연결용

from app.database import engine, Base, get_db
from app import models # 모델 가져오기
from app.routers import users, system
from app.core.scheduler import start_scheduler
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 템플릿(HTML) 폴더 지정
templates = Jinja2Templates(directory="templates")

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    start_scheduler()
    yield

app = FastAPI(
    title="베지나이 1.0",
    lifespan=lifespan
)

app.include_router(users.router)
app.include_router(system.router)

# [NEW] 대시보드 화면 라우터 (접속 주소: http://localhost:8000/dashboard)
@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request, db: Session = Depends(get_db)):
    # DB에서 모든 사장님 정보를 가져와서 HTML로 넘겨줍니다.
    users = db.query(models.User).all()
    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={"users": users}
    )

# 루트 접속 시 대시보드로 안내
@app.get("/")
def read_root():
    return HTMLResponse('<a href="/dashboard">👉 관리자 대시보드 바로가기</a>')