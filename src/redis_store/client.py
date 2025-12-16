import redis
from src.config.env import EnvConfig

_redis_client_instance = None


def get_redis_client():
    global _redis_client_instance

    if _redis_client_instance is not None:
        return _redis_client_instance

    _redis_client_instance = redis.Redis(
        host=EnvConfig.REDIS_HOST,
        port=EnvConfig.REDIS_PORT,
        ssl=EnvConfig.REDIS_SSL_ENABLED,
        decode_responses=True,
    )
    return _redis_client_instance
