# 파일명: setup_env.py
import os

content = """TOSS_API_KEY=waiting_for_approval

# [Solapi 설정]
SOLAPI_API_KEY=NCS4COIDQ681XXPL
SOLAPI_API_SECRET=4IWZDH2PMMQJXBZRDRA5Z7SQUTP8VFSX

SENDER_PHONE=01021123558
# ▲ 솔라피 사이트 [발신번호 관리]에 등록된 본인 휴대폰 번호 (- 제외)

DATABASE_URL=sqlite:///./sales_bot.db

MANAGER_PHONE=01021123558
# ▲ 리포트를 받아볼 본인(매니저) 휴대폰 번호 (- 제외)
"""

with open(".env", "w", encoding="utf-8") as f:
    f.write(content)

print("✅ .env 파일이 생성되었습니다.")