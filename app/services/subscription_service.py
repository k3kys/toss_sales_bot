from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app import models
from app.services.kakao_client import KakaoClient
import logging

logger = logging.getLogger(__name__)


class SubscriptionService:
    # [TODO] 사장님이 만드신 구글폼 링크를 여기에 넣으세요
    GOOGLE_FORM_URL = "https://forms.google.com/your-form-link"

    @staticmethod
    def check_and_notify_expiration():
        """
        만료일이 '내일'인 사용자를 찾아 연장 안내 메시지를 보냅니다.
        """
        logger.info("🔍 [Subscription] 만료 임박 사용자 스캔 시작")

        db: Session = SessionLocal()
        kakao = KakaoClient()

        try:
            # 내일 날짜 구하기 (시간 무시하고 날짜만 비교하기 위해 범위 설정)
            tomorrow = datetime.now() + timedelta(days=1)
            start_of_tomorrow = tomorrow.replace(hour=0, minute=0, second=0, microsecond=0)
            end_of_tomorrow = tomorrow.replace(hour=23, minute=59, second=59, microsecond=999999)

            # 만료일이 내일인 사람 찾기
            expiring_users = db.query(models.User).filter(
                models.User.expiration_date >= start_of_tomorrow,
                models.User.expiration_date <= end_of_tomorrow
            ).all()

            if not expiring_users:
                logger.info("✅ 내일 만료 예정인 사용자가 없습니다.")
                return

            for user in expiring_users:
                SubscriptionService._send_renewal_message(kakao, user)

        except Exception as e:
            logger.error(f"❌ [Subscription] 만료 체크 중 오류: {str(e)}")
        finally:
            db.close()

    @staticmethod
    def _send_renewal_message(kakao_client, user):
        """연장 권유 카톡 발송"""
        msg = f"""[베지나이 1.0]
⏳ 무료 체험판 만료 예정 안내

안녕하세요, {user.username} 사장님!
서비스 이용은 만족스러우셨나요?

사장님의 무료 체험 기간이 **내일({user.expiration_date.strftime('%m월 %d일')})** 종료됩니다.

매출 보고가 끊기지 않도록, 아래 링크에서 기간을 연장해주세요.

👉 **기간 연장 신청하기:**
{SubscriptionService.GOOGLE_FORM_URL}

(내일까지 연장하지 않으시면 모레부터 자동 리포트가 전송되지 않습니다.)"""

        try:
            kakao_client.send_message(uuid=user.kakao_uuid, message=msg)
            logger.info(f"📩 {user.username} 님에게 연장 안내 발송 완료")
        except Exception as e:
            logger.error(f"❌ {user.username} 연장 안내 발송 실패: {e}")