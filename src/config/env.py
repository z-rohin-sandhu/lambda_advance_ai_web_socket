import os
from src.constants.redis_keys import (
    DEFAULT_CONNECTION_TTL_SECONDS,
    DEFAULT_SESSION_TTL_SECONDS,
)

class EnvConfig:
    REDIS_HOST = os.environ.get("REDIS_HOST", "localhost")
    REDIS_PORT = int(os.environ.get("REDIS_PORT", 6379))
    REDIS_SSL_ENABLED = os.environ.get("REDIS_SSL", "false").lower() == "true"

    REDIS_CONNECTION_TTL_SECONDS = int(
        os.environ.get("REDIS_CONN_TTL", DEFAULT_CONNECTION_TTL_SECONDS)
    )
    REDIS_SESSION_TTL_SECONDS = int(
        os.environ.get("REDIS_SESSION_TTL", DEFAULT_SESSION_TTL_SECONDS)
    )
