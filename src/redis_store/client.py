# src/redis_store/client.py

import traceback
import redis

from src.config.base import BaseConfig
from src.utils.logging import log

def get_client():
    try:
        log("Redis initializing client")
        client = redis.Redis(
            host=BaseConfig.REDIS_HOST,
            port=BaseConfig.REDIS_PORT,
            ssl=BaseConfig.REDIS_SSL,
            db=BaseConfig.REDIS_DATABASE_INDEX,
            decode_responses=True,
        )
        client.ping()
        log("Redis connection successful")
        return client
    except Exception:
        log("Redis connection failed", level="ERROR")
        log(traceback.format_exc(), level="ERROR")
        return None
