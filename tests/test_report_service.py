from unittest.mock import patch, MagicMock, call
from app.services.report_service import ReportService


# ------------------------------------------------------------------
# CASE 1: 특정 매장(파체리토)만 토스 조회가 실패했을 때
# ------------------------------------------------------------------
def test_partial_toss_failure(db_session, seed_users):
    with patch("app.services.report_service.TossClient") as MockToss, \
            patch("app.services.report_service.KakaoClient") as MockKakao, \
            patch("app.services.report_service.SessionLocal") as mock_db_maker:
        mock_db_maker.return_value = db_session
        toss_instance = MockToss.return_value

        # [시나리오] 2번째 호출(파체리토)에서만 에러
        toss_instance.get_sales_data.side_effect = [
            {"total": 100, "hall": 100, "baemin": 0, "coupang": 0, "yogiyo": 0},
            Exception("Toss API Error"),
            {"total": 200, "hall": 200, "baemin": 0, "coupang": 0, "yogiyo": 0},
        ]

        ReportService.execute_daily_report()

        kakao_instance = MockKakao.return_value
        calls = kakao_instance.send_message.call_args_list

        # 파체리토(uuid_2)에게 '자동 매출 보고 실패' 알림이 갔는지 확인
        error_alert_sent = any("uuid_2" in str(c) and "자동 매출 보고 실패" in str(c) for c in calls)
        assert error_alert_sent is True, "파체리토에게 수동 보고 요청이 전송되지 않았습니다."


# ------------------------------------------------------------------
# CASE 2: 매니저에게 통합 리포트 전송이 실패했을 때 (전체 비상)
# ------------------------------------------------------------------
def test_manager_send_failure(db_session, seed_users):
    with patch("app.services.report_service.TossClient") as MockToss, \
            patch("app.services.report_service.KakaoClient") as MockKakao, \
            patch("app.services.report_service.SessionLocal") as mock_db_maker:

        mock_db_maker.return_value = db_session
        toss_instance = MockToss.return_value
        # 토스 데이터 조회는 모두 성공한다고 가정
        toss_instance.get_sales_data.return_value = {"total": 100, "hall": 0, "baemin": 0, "coupang": 0, "yogiyo": 0}

        kakao_instance = MockKakao.return_value

        # [핵심 수정] 에러 트리거 조건 변경
        def kakao_side_effect(uuid=None, message=""):
            # 매니저(test_manager_uuid)에게 '매출 데이터(일일매출)'를 보낼 때만 에러 발생
            # (시스템 장애 알림은 정상적으로 보내야 함)
            if uuid == "test_manager_uuid" and "일일매출" in message:
                raise Exception("Network Error")
            print(f"Mock Send to {uuid}")

        kakao_instance.send_message.side_effect = kakao_side_effect

        ReportService.execute_daily_report()

        calls = kakao_instance.send_message.call_args_list

        # 1. 매니저에게 '시스템 장애 알림'이 갔는지?
        manager_notice = any("시스템 장애 알림" in str(c) for c in calls)
        assert manager_notice is True, "매니저에게 장애 알림이 가지 않았습니다."

        # 2. 모든 사장님에게 '비상 요청'이 갔는지?
        user_uuids = ["uuid_1", "uuid_2", "uuid_3"]
        for uid in user_uuids:
            sent = any(uid in str(c) and "자동 매출 보고 실패" in str(c) for c in calls)
            assert sent is True, f"{uid} 사장님에게 비상 알림이 누락되었습니다."