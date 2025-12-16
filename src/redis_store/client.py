# src/redis_store/client.py

import traceback
import redis as redis_library

from src.config.base import BaseConfig


class RedisClient:
    @staticmethod
    def get_client():
        try:
            print("[Redis] Initializing Redis client")
            client = redis_library.Redis(
                host=BaseConfig.REDIS_HOST,
                port=BaseConfig.REDIS_PORT,
                ssl=BaseConfig.REDIS_SSL,
                db=BaseConfig.REDIS_DATABASE_INDEX,
                decode_responses=True,
            )
            client.ping()
            print("[Redis] Redis connection successful")
            return client
        except Exception:
            print("[Redis] Redis connection failed")
            print(traceback.format_exc())
            return None
