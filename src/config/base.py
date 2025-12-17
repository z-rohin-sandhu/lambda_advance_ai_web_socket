from src.config.env import get_env
from src.constants.redis_keys import (
    DEFAULT_CONNECTION_TTL_SECONDS,
    DEFAULT_SESSION_TTL_SECONDS_SECONDS
)
from src.constants.aws import DEFAULT_AWS_REGION



class BaseConfig:
    # Runtime
    APP_ENV = get_env("APP_ENV", "dev")
    AWS_REGION = get_env("AWS_REGION", DEFAULT_AWS_REGION)
    LOG_LEVEL = get_env("LOG_LEVEL", "INFO")

    # Redis
    REDIS_HOST = get_env("REDIS_HOST", "localhost")
    REDIS_PORT = int(get_env("REDIS_PORT", 6379))
    REDIS_SSL = get_env("REDIS_SSL", "false").lower() == "true"
    REDIS_DATABASE_INDEX = int(get_env("REDIS_DATABASE_INDEX", 0))

    # TTLs
    CONNECTION_TTL_SECONDS = int(get_env("CONNECTION_TTL_SECONDS", DEFAULT_CONNECTION_TTL_SECONDS))
    SESSION_TTL_SECONDS = int(get_env("SESSION_TTL_SECONDS", DEFAULT_SESSION_TTL_SECONDS_SECONDS))
    REDIS_ENABLED = get_env("REDIS_ENABLED", "false").lower() == "true"