# app/routers/users.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timedelta

from app.database import get_db
from app import models, schemas

router = APIRouter(prefix="/users", tags=["Users"])


# --- [Helper] 만료일 계산기 ---
def calculate_expiration(plan: schemas.PlanType) -> datetime:
    now = datetime.now()
    if plan == schemas.PlanType.TRIAL:
        return now + timedelta(days=7)
    elif plan == schemas.PlanType.MONTH_3:
        return now + timedelta(days=90)
    elif plan == schemas.PlanType.MONTH_6:
        return now + timedelta(days=180)
    elif plan == schemas.PlanType.YEAR_1:
        return now + timedelta(days=365)
    elif plan == schemas.PlanType.YEAR_2:
        return now + timedelta(days=365 * 2)
    elif plan == schemas.PlanType.UNLIMITED:
        return datetime(9999, 12, 31)  # 사실상 무제한
    return now  # 기본값


# 1. [Create] 사장님 등록 (구독 유형 선택 가능)
@router.post("/", response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="이미 등록된 매장명입니다.")

    # 플랜에 따른 만료일 자동 계산
    expire_at = calculate_expiration(user.plan_type)

    new_user = models.User(
        username=user.username,
        toss_token=user.toss_token,
        phone_number=user.phone_number,
        plan_type=user.plan_type.value,
        expiration_date=expire_at
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


# 2. [Read] 전체 사장님 조회
@router.get("/", response_model=List[schemas.UserResponse])
def read_users(db: Session = Depends(get_db)):
    return db.query(models.User).all()


# 3. [Update] 사장님 정보 수정 (플랜 변경 시 기간 연장) - [NEW]
@router.put("/{user_id}", response_model=schemas.UserResponse)
def update_user(user_id: int, user_update: schemas.UserUpdate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다.")

    # 정보 업데이트
    if user_update.toss_token:
        db_user.toss_token = user_update.toss_token

    if user_update.phone_number:
        db_user.phone_number = user_update.phone_number

    # 플랜 변경 요청이 오면 만료일을 새로 계산해서 갱신
    if user_update.plan_type:
        db_user.plan_type = user_update.plan_type.value
        db_user.expiration_date = calculate_expiration(user_update.plan_type)

    db.commit()
    db.refresh(db_user)
    return db_user


# 4. [Delete] 사장님 삭제 (서비스 중단) - [NEW]
@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다.")

    db.delete(db_user)
    db.commit()
    return {"message": f"{db_user.username} 사장님 정보를 삭제했습니다."}