from apscheduler.schedulers.background import BackgroundScheduler
from app.services.report_service import ReportService
from app.services.backup_service import BackupService
from app.services.subscription_service import SubscriptionService  # [New] 추가
import logging

logger = logging.getLogger(__name__)


def start_scheduler():
    scheduler = BackgroundScheduler()

    # 1. 매일 21시 57분: 일일 매출 리포트 전송
    scheduler.add_job(
        ReportService.execute_daily_report,
        'cron',
        hour=21,
        minute=57,
        id='daily_sales_report'
    )

    # 2. 매일 새벽 04시 00분: DB 백업
    scheduler.add_job(
        BackupService.create_backup,
        'cron',
        hour=4,
        minute=00,
        id='db_daily_backup'
    )

    # 3. [New] 매일 낮 12시 00분: 만료 임박자(D-1) 연장 안내 발송
    scheduler.add_job(
        SubscriptionService.check_and_notify_expiration,
        'cron',
        hour=12,
        minute=00,
        id='subscription_check'
    )

    scheduler.start()
    logger.info('⏰ [Scheduler] 리포트(21:57), 백업(04:00), 구독체크(12:00) 가동됨')