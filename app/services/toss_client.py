# app/services/toss_client.py
class TossClient:
    def __init__(self, api_key=None):
        self.api_key = api_key

    # [수정] query_date 파라미터 추가!
    def get_sales_data(self, query_date=None):
        # 지금은 API 연결 없이 테스트용 가짜 데이터를 반환합니다.
        # query_date를 받아주기만 하고 사용은 안 함 (나중에 사용 예정)
        print(f"📡 [Toss] {query_date} 매출 데이터를 조회합니다...")

        return {
            "total": 500000,
            "hall": 300000,
            "baemin": 150000,
            "coupang": 50000,
            "yogiyo": 0
        }