from fastapi import FastAPI
from datetime import datetime, timezone

app = FastAPI(title="Server Time API")


@app.get("/")
def root():
    return {"message": "Server Time API is running. Visit /time or /date for server time and date."}


@app.get("/time")
def get_server_time():
    now = datetime.now()
    now_utc = datetime.now(timezone.utc)
    return {
        "local_time": now.isoformat(),
        "utc_time": now_utc.isoformat(),
        "timestamp": now_utc.timestamp(),
    }


@app.get("/date")
def get_server_date():
    now = datetime.now()
    now_utc = datetime.now(timezone.utc)
    return {
        "local_date": now.date().isoformat(),
        "utc_date": now_utc.date().isoformat(),
        "day": now.day,
        "month": now.month,
        "year": now.year,
        "weekday": now.strftime("%A"),
        "weekday_short": now.strftime("%a"),
    }


@app.get("/datetime")
def get_server_datetime():
    now = datetime.now()
    now_utc = datetime.now(timezone.utc)
    return {
        "local_date": now.date().isoformat(),
        "local_time": now.time().isoformat(),
        "utc_date": now_utc.date().isoformat(),
        "utc_time": now_utc.time().isoformat(),
        "timestamp": now_utc.timestamp(),
        "weekday": now.strftime("%A"),
    }
