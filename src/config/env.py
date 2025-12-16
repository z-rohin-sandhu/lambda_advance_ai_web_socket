import os
from src.constants.redis_keys import (
    DEFAULT_CONNECTION_TTL_SECONDS,
    DEFAULT_SESSION_TTL_SECONDS_SECONDS,
)


def get_env(name: str, default=None):
    value = os.environ.get(name)
    return value if value is not None else default
    

class EnvConfig:
    REDIS_HOST = get_env("REDIS_HOST", "localhost")
    REDIS_PORT = int(get_env("REDIS_PORT", 6379))
    REDIS_SSL_ENABLED = get_env("REDIS_SSL", "false").lower() == "true"

    REDIS_CONNECTION_TTL_SECONDS = int(
        get_env("REDIS_CONNECTION_TTL_SECONDS", DEFAULT_CONNECTION_TTL_SECONDS)
    )
    REDIS_SESSION_TTL_SECONDS_SECONDS = int(
        get_env("REDIS_SESSION_TTL_SECONDS", DEFAULT_SESSION_TTL_SECONDS_SECONDS)
    )
