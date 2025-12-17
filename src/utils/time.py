import time
from datetime import datetime, timezone


def current_timestamp() -> int:
    return int(time.time())


def current_datetime_utc() -> str:
    return datetime.now(timezone.utc).isoformat()

