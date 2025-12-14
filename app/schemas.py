# app/schemas.py
from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from enum import Enum

# 1. 구독 유형 정의 (오타 방지용)
class PlanType(str, Enum):
    TRIAL = "TRIAL"       # 7일
    MONTH_3 = "3M"        # 3개월
    MONTH_6 = "6M"        # 6개월
    YEAR_1 = "1Y"         # 1년
    YEAR_2 = "2Y"         # 2년
    UNLIMITED = "UNLIMITED" # 무제한

# 2. 사장님 등록 양식 (Create)
class UserCreate(BaseModel):
    username: str
    toss_token: str = "dummy_token"
    phone_number: str
    plan_type: PlanType = PlanType.TRIAL  # 기본값은 체험판

# 3. 사장님 정보 수정 양식 (Update) - [NEW]
# 입력하지 않은 정보는 기존 정보를 유지하기 위해 Optional 사용
class UserUpdate(BaseModel):
    toss_token: Optional[str] = None
    phone_number: Optional[str] = None
    plan_type: Optional[PlanType] = None  # 플랜을 변경하면 만료일이 자동 갱신됨

# 4. 응답 양식 (Response)
class UserResponse(BaseModel):
    id: int
    username: str
    phone_number: str
    plan_type: str        # 어떤 플랜인지
    expiration_date: Optional[datetime] # 언제 만료되는지
    created_at: datetime

    class Config:
        from_attributes = True