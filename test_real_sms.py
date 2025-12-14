# test_real_sms.py
import sys
import os

# 현재 폴더를 파이썬 경로에 추가 (모듈 import 에러 방지)
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.config import settings
from app.services.solapi_client import SolapiClient

def test_sms_now():
    print("="*40)
    print("🚀 [솔라피] 리얼 문자 발송 테스트 시작")
    print("="*40)

    # 1. 설정 확인
    print(f"📡 받는 사람(매니저): {settings.MANAGER_PHONE}")
    print(f"📡 보내는 사람(나)  : {settings.SENDER_PHONE}")
    print(f"🔑 API KEY 앞4자리: {settings.SOLAPI_API_KEY[:4]}****")

    # 2. 클라이언트 생성
    client = SolapiClient()

    # 3. 보낼 메시지
    message = """[베지나이 테스트]
이 문자가 보이면 성공입니다! 🎉
솔라피 연동이 완벽하게 되었습니다.
- 시스템 관리자 드림 -"""

    # 4. 발송 시도
    print("\n📨 문자를 전송하는 중입니다...")
    result = client.send_message(to_number=settings.MANAGER_PHONE, message=message)

    if result:
        print("\n✅ [성공] 핸드폰 문자를 확인해보세요!")
    else:
        print("\n❌ [실패] .env 파일의 키 설정이나 잔액을 확인해주세요.")

if __name__ == "__main__":
    test_sms_now()