# 1. 파이썬 3.11 슬림 버전 (가볍고 빠름)
FROM python:3.11-slim

# 2. 작업 폴더 설정
WORKDIR /app

# 3. 환경 변수 설정
# - 파이썬 로그가 버퍼링 없이 즉시 출력되도록 설정
# - .pyc 파일 생성 방지
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
# - [중요] 한국 시간대 설정 (이거 없으면 9시간 차이 남)
ENV TZ=Asia/Seoul

# 4. 시스템 패키지 설치 (시간대 설정용 tzdata 등)
RUN apt-get update && apt-get install -y \
    tzdata \
    && ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone \
    && rm -rf /var/lib/apt/lists/*

# 5. 라이브러리 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 6. 소스 코드 복사
COPY . .

# 7. 포트 개방
EXPOSE 8000

# 8. 서버 실행 (앱 시작)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]