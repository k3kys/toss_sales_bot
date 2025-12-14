# run.py
import uvicorn

if __name__ == "__main__":
    # reload=True로 설정하여 코드 수정 시 자동 재시작
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)