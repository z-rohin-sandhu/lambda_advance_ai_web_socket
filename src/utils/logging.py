from typing import Literal
from src.utils.time import current_datetime_utc


LogLevel = Literal["INFO", "ERROR", "DEBUG", "WARN"]


def log(message: str, level: LogLevel = "INFO", **context: dict):
    timestamp = current_datetime_utc()

    if context and isinstance(context, dict):
        print(
            f"{timestamp} [{level}] {message} | "
            f"{', '.join(f'{key}={value}' for key, value in context.items())}"
        )
    else:
        print(f"{timestamp} [{level}] {message}")