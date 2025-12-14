import shutil
import os
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class BackupService:
    @staticmethod
    def create_backup():
        # --- 1. 경로 설정 ---
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        db_path = os.path.join(base_dir, "sales_bot.db")
        backup_dir = os.path.join(base_dir, "backups")

        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)

        # --- 2. 백업 수행 ---
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_filename = f"sales_bot_{timestamp}.db"
        backup_path = os.path.join(backup_dir, backup_filename)

        try:
            if os.path.exists(db_path):
                shutil.copy2(db_path, backup_path)
                logger.info(f"✅ [Backup] DB 백업 완료: {backup_filename}")

                # --- 3. [핵심] 청소 로직 (Rotation) ---
                BackupService.cleanup_old_backups(backup_dir, keep_count=3)

                return backup_filename
            else:
                logger.warning("⚠️ [Backup] 원본 DB 파일을 찾을 수 없습니다.")
        except Exception as e:
            logger.error(f"❌ [Backup] 작업 실패: {str(e)}")

    @staticmethod
    def cleanup_old_backups(backup_dir, keep_count=3):
        """
        오래된 백업 파일을 삭제하여 최신 N개만 유지합니다.
        """
        try:
            # 폴더 내 모든 파일 리스트업
            files = [os.path.join(backup_dir, f) for f in os.listdir(backup_dir)
                     if os.path.isfile(os.path.join(backup_dir, f))]

            # 생성 시간순 정렬 (오래된 것 -> 최신 것)
            files.sort(key=os.path.getmtime)

            # 파일 개수가 기준보다 많으면, 오래된 것부터 삭제
            while len(files) > keep_count:
                oldest_file = files.pop(0)  # 맨 앞(가장 오래된 것) 꺼내기
                os.remove(oldest_file)
                logger.info(f"🗑️ [Backup] 오래된 백업 삭제됨: {os.path.basename(oldest_file)}")

        except Exception as e:
            logger.error(f"⚠️ [Backup] 청소 중 오류 발생: {str(e)}")