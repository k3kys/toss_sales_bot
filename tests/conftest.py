# tests/conftest.py
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base
from app import models

# 1. 테스트용 인메모리 DB (파일생성 X, RAM 사용)
TEST_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# 2. DB 세션 피스처 (각 테스트마다 깨끗한 DB 제공)
@pytest.fixture(scope="function")
def db_session():
    # 테이블 생성
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()

    yield session  # 테스트 실행 중에는 이 세션을 사용

    # 테스트 끝나면 정리
    session.close()
    Base.metadata.drop_all(bind=engine)


# 3. 더미 데이터 피스처 (사장님 3명 미리 심어놓기)
@pytest.fixture(scope="function")
def seed_users(db_session):
    users = [
        models.User(username="베지나랑", toss_token="token_1", kakao_uuid="uuid_1"),
        models.User(username="파체리토", toss_token="token_2", kakao_uuid="uuid_2"),
        models.User(username="군초밥", toss_token="token_3", kakao_uuid="uuid_3"),
    ]
    db_session.add_all(users)
    db_session.commit()
    return users