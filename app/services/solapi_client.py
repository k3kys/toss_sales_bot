import uuid
import hmac
import hashlib
import requests
import logging
from datetime import datetime
from app.core.config import settings

logger = logging.getLogger(__name__)


class SolapiClient:
    """
    솔라피(CoolSMS) 문자 발송 클라이언트 (v4 API)
    """
    BASE_URL = "https://api.solapi.com/messages/v4/send"

    def __init__(self):
        # 여기서 설정값들을 불러옵니다. 이 부분이 빠져서 에러가 났던 것입니다.
        self.api_key = settings.SOLAPI_API_KEY
        self.api_secret = settings.SOLAPI_API_SECRET
        self.sender = settings.SENDER_PHONE

    def _get_headers(self):
        """API 인증 헤더 생성 (HMAC-SHA256 방식)"""
        date = datetime.now().isoformat()
        salt = str(uuid.uuid4().hex)
        data = date + salt
        signature = hmac.new(
            key=self.api_secret.encode("utf-8"),
            msg=data.encode("utf-8"),
            digestmod=hashlib.sha256
        ).hexdigest()

        return {
            "Authorization": f"HMAC-SHA256 apiKey={self.api_key}, date={date}, salt={salt}, signature={signature}",
            "Content-Type": "application/json"
        }

    def send_message(self, to_number: str, message: str, subject: str = None):
        """
        문자 발송 (LMS 장문)
        - subject: 문자 제목 (선택사항)
        """
        if not to_number:
            logger.warning("⚠️ 수신자 번호가 없습니다.")
            return False

        payload = {
            "message": {
                "to": to_number,
                "from": self.sender,
                "text": message,
                "subject": subject,  # 제목 추가
                "type": "LMS"  # 장문 메시지
            }
        }

        try:
            res = requests.post(self.BASE_URL, headers=self._get_headers(), json=payload)

            if res.status_code == 200:
                logger.info(f"✅ [Solapi] 문자 전송 성공 (To: {to_number})")
                return True
            else:
                logger.error(f"❌ [Solapi] 전송 실패: {res.json()}")
                return False

        except Exception as e:
            logger.error(f"❌ [Solapi] 연결 에러: {str(e)}")
            return False