from fastapi import APIRouter
from app.services.backup_service import BackupService
from app.services.report_service import ReportService

router = APIRouter(prefix="/system", tags=["System"])

@router.post("/backup")
def manual_backup():
    filename = BackupService.create_backup()
    return {"status": "success", "file": filename}

@router.post("/report")
def manual_report():
    ReportService.execute_daily_report()
    return {"status": "success", "message": "리포트 발송 요청됨"}
