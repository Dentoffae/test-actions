from fastapi import FastAPI, HTTPException, Query
from datetime import datetime, timezone
import pytz

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


TIMEZONE_ALIASES: dict[str, str] = {
    # Россия
    "москва": "Europe/Moscow",
    "moscow": "Europe/Moscow",
    "санкт-петербург": "Europe/Moscow",
    "петербург": "Europe/Moscow",
    "екатеринбург": "Asia/Yekaterinburg",
    "yekaterinburg": "Asia/Yekaterinburg",
    "ekaterinburg": "Asia/Yekaterinburg",
    "новосибирск": "Asia/Novosibirsk",
    "novosibirsk": "Asia/Novosibirsk",
    "омск": "Asia/Omsk",
    "omsk": "Asia/Omsk",
    "красноярск": "Asia/Krasnoyarsk",
    "krasnoyarsk": "Asia/Krasnoyarsk",
    "иркутск": "Asia/Irkutsk",
    "irkutsk": "Asia/Irkutsk",
    "якутск": "Asia/Yakutsk",
    "yakutsk": "Asia/Yakutsk",
    "владивосток": "Asia/Vladivostok",
    "vladivostok": "Asia/Vladivostok",
    "магадан": "Asia/Magadan",
    "magadan": "Asia/Magadan",
    "камчатка": "Asia/Kamchatka",
    "kamchatka": "Asia/Kamchatka",
    "самара": "Europe/Samara",
    "samara": "Europe/Samara",
    "челябинск": "Asia/Yekaterinburg",
    "chelyabinsk": "Asia/Yekaterinburg",
    "калининград": "Europe/Kaliningrad",
    "kaliningrad": "Europe/Kaliningrad",
    # Мировые города
    "лондон": "Europe/London",
    "london": "Europe/London",
    "берлин": "Europe/Berlin",
    "berlin": "Europe/Berlin",
    "париж": "Europe/Paris",
    "paris": "Europe/Paris",
    "рим": "Europe/Rome",
    "rome": "Europe/Rome",
    "токио": "Asia/Tokyo",
    "tokyo": "Asia/Tokyo",
    "пекин": "Asia/Shanghai",
    "beijing": "Asia/Shanghai",
    "шанхай": "Asia/Shanghai",
    "shanghai": "Asia/Shanghai",
    "дубай": "Asia/Dubai",
    "dubai": "Asia/Dubai",
    "нью-йорк": "America/New_York",
    "new york": "America/New_York",
    "newyork": "America/New_York",
    "лос-анджелес": "America/Los_Angeles",
    "los angeles": "America/Los_Angeles",
    "чикаго": "America/Chicago",
    "chicago": "America/Chicago",
    "сидней": "Australia/Sydney",
    "sydney": "Australia/Sydney",
    "стамбул": "Europe/Istanbul",
    "istanbul": "Europe/Istanbul",
    "сеул": "Asia/Seoul",
    "seoul": "Asia/Seoul",
    "дели": "Asia/Kolkata",
    "delhi": "Asia/Kolkata",
}


def resolve_timezone(tz_input: str) -> pytz.BaseTzInfo:
    key = tz_input.strip().lower()
    iana_name = TIMEZONE_ALIASES.get(key, tz_input.strip())
    try:
        return pytz.timezone(iana_name)
    except pytz.UnknownTimeZoneError:
        available = sorted(TIMEZONE_ALIASES.keys())
        raise HTTPException(
            status_code=400,
            detail={
                "error": f"Неизвестный часовой пояс: '{tz_input}'",
                "hint": "Используй название города или IANA-зону (например Europe/Moscow)",
                "available_cities": available,
            },
        )


@app.get("/convert")
def convert_timezone(
    time: str = Query(..., description="Время в UTC, формат HH:MM или HH:MM:SS", examples=["15:00"]),
    tz: str = Query(..., description="Часовой пояс: город или IANA-зона", examples=["Екатеринбург"]),
):
    formats = ["%H:%M", "%H:%M:%S", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%d %H:%M:%S"]
    utc_dt = None
    for fmt in formats:
        try:
            parsed = datetime.strptime(time.strip(), fmt)
            today = datetime.utcnow().date()
            utc_dt = datetime(today.year, today.month, today.day,
                              parsed.hour, parsed.minute, parsed.second,
                              tzinfo=pytz.utc)
            break
        except ValueError:
            continue

    if utc_dt is None:
        raise HTTPException(
            status_code=400,
            detail={"error": f"Не удалось распознать время: '{time}'", "hint": "Используй формат HH:MM или HH:MM:SS"},
        )

    target_tz = resolve_timezone(tz)
    converted = utc_dt.astimezone(target_tz)
    offset = converted.utcoffset()
    offset_hours = int(offset.total_seconds() // 3600)
    offset_str = f"UTC{'+' if offset_hours >= 0 else ''}{offset_hours}"

    return {
        "input_utc": utc_dt.strftime("%H:%M:%S"),
        "timezone": str(target_tz),
        "offset": offset_str,
        "converted_time": converted.strftime("%H:%M:%S"),
        "converted_datetime": converted.isoformat(),
    }
