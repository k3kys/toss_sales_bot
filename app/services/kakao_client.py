class KakaoClient:
    def send_message(self, message: str):
        # 실제 전송 대신 터미널에 프린트합니다.
        print("\n🟡 [Kakao] 알림톡 발송 요청 도착!")
        print("---------------------------------")
        print(message)
        print("---------------------------------\n")