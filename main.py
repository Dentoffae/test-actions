from fastapi import FastAPI
from datetime import datetime, timezone

app = FastAPI(title="Server Time API")


@app.get("/")
def root():
    return {"message": "Server Time API is running. Visit /time to get the current server time."}


@app.get("/time")
def get_server_time():
    now = datetime.now()
    now_utc = datetime.now(timezone.utc)
    return {
        "local_time": now.isoformat(),
        "utc_time": now_utc.isoformat(),
        "timestamp": now_utc.timestamp(),
    }
