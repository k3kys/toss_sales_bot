# app/models.py
from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    toss_token = Column(String)

    # [핵심] 여기가 꼭 'phone_number'여야 합니다!
    phone_number = Column(String)

    plan_type = Column(String, default="TRIAL")
    expiration_date = Column(DateTime)
    created_at = Column(DateTime, default=datetime.now)