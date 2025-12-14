from datetime import datetime
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app import models
from app.services.toss_client import TossClient
from app.services.solapi_client import SolapiClient
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)


class ReportService:
    @staticmethod
    def execute_daily_report():
        logger.info("🚀 [Batch] 통합 리포트 생성 시작")

        db: Session = SessionLocal()
        messenger = SolapiClient()

        # 날짜 포맷 (예: 12월 3일)
        now = datetime.now()
        date_header = f"{now.month}월 {now.day}일"
        query_date = now.strftime("%Y-%m-%d")

        store_reports = []

        try:
            users = db.query(models.User).all()

            for user in users:
                try:
                    # 구독 만료 체크
                    if user.expiration_date and user.expiration_date < now:
                        continue

                    # 토스 데이터 조회
                    toss = TossClient(api_key=user.toss_token)
                    data = toss.get_sales_data(query_date)

                    # [요청하신 양식 그대로 적용]
                    report_block = f"""{user.username}
{date_header} 일일매출
총 : {data['total']:,}

홀 :  {data['hall']:,}
배민 : {data['baemin']:,}
쿠팡 : {data['coupang']:,}
요기요 : {data['yogiyo']:,}
입니다."""

                    store_reports.append(report_block)

                except Exception as e:
                    logger.error(f"⚠️ {user.username} 조회 실패: {e}")
                    ReportService._send_user_alert(messenger, user, "데이터 조회 실패")

            if not store_reports:
                return

            # [최종 메시지 조립]
            # 매장별 리포트를 줄바꿈 두 번으로 연결 (구분선 없음)
            final_message = "\n\n".join(store_reports)

            # [제목] 문자 목록용 제목 (내용엔 영향 없음)
            report_title = f"[베지나이1.0] {date_header} 매출 보고"

            # 전송
            logger.info(f"📤 통합 리포트 전송 (To: {settings.MANAGER_PHONE})")
            messenger.send_message(
                to_number=settings.MANAGER_PHONE,
                message=final_message,
                subject=report_title
            )

        except Exception as e:
            logger.error(f"❌ [System] 오류: {str(e)}")
        finally:
            db.close()

    @staticmethod
    def _send_user_alert(messenger, user, reason):
        title = "🚨 전송 실패 알림"
        msg = f"""{user.username} 사장님
시스템 오류로 자동 보고가 전송되지 않았습니다. ({reason})
매니저에게 문의해주세요."""

        messenger.send_message(
            to_number=user.phone_number,
            message=msg,
            subject=title
        )