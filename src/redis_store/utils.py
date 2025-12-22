from src.config.base import BaseConfig
from src.utils.logging import log
from src.utils.json_utils import json_dumps

import redis, traceback

class Redis:
    @staticmethod
    def get_redis_client():
        """
        Establishes a Redis client connection.
        """
        try:
            data = BaseConfig.get_db_configuration_details(db_type="redis")
            host, ssl, port = data.get("host"), data.get("ssl"), data.get("port")
            redis_client = redis.Redis(host=host, port=port, ssl=ssl)

            return redis_client
        except Exception as e:
            log("get_redis_client failed", level="ERROR", error=str(e))
            log(traceback.format_exc(), level="ERROR")
            return None

    @staticmethod
    def get_value_from_redis(redis_client=None, key=None):
        """
        Retrieves a value from Redis.
        """
        value = None  # Ensure value is initialized
        try:
            if not redis_client:
                redis_client = Redis.get_redis_client()

            value = redis_client.get(key)
            value = value.decode('utf-8') if value else None

        except Exception as e:
            log("get_value_from_redis failed", level="ERROR", error=str(e))
            log(traceback.format_exc(), level="ERROR")
        
        return value

    @staticmethod
    def insert_into_redis(redis_client=None, key=None, data={}, redis_expiry=3600):
        """
        Inserts a key-value pair into Redis with an expiration time.
        """
        try:
            if not redis_client:
                redis_client = Redis.get_redis_client()
            data = json_dumps(data)
            redis_client.set(key, data, ex=redis_expiry)
            log("insert_into_redis success", key=key, data=data, redis_expiry=redis_expiry)
        
        except Exception as e:
            log("insert_into_redis failed", level="ERROR", error=str(e))
            log(traceback.format_exc(), level="ERROR")
        

    @staticmethod
    def delete_redis_key(redis_client=None, key=None):
        """
        Deletes a key from Redis.
        """
        try:
            if not redis_client:
                redis_client = Redis.get_redis_client()
            redis_client.delete(key)
            log("delete_redis_key success", key=key)
        except Exception as e:
            log("delete_redis_key failed", level="ERROR", error=str(e))
            log(traceback.format_exc(), level="ERROR")