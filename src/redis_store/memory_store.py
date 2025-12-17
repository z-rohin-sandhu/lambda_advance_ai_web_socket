from typing import Any, Dict, Optional

from src.utils.json_utils import json_dumps, json_loads
from src.utils.time import current_timestamp


class InMemoryRedis:
    """
    Temporary in-memory Redis replacement.
    This is ONLY used when REDIS_ENABLED = false.
    """

    _STORE: Dict[str, Dict[str, Any]] = {}

    @classmethod
    def set(cls, key: str, value: dict, ttl_seconds: int) -> None:
        expires_at = current_timestamp() + ttl_seconds

        cls._STORE[key] = {
            "value": json_dumps(value),
            "expires_at": expires_at,
        }

        print(
            "[InMemoryRedis.set] "
            f"key={key}, ttl={ttl_seconds}, expires_at={expires_at}"
        )

    @classmethod
    def get(cls, key: str) -> Optional[dict]:
        record = cls._STORE.get(key)

        if not record:
            print(f"[InMemoryRedis.get] key={key} NOT FOUND")
            return None

        if record["expires_at"] < current_timestamp():
            print(f"[InMemoryRedis.get] key={key} EXPIRED")
            cls._STORE.pop(key, None)
            return None

        print(f"[InMemoryRedis.get] key={key} HIT")
        return json_loads(record["value"])

    @classmethod
    def delete(cls, key: str) -> None:
        existed = key in cls._STORE
        cls._STORE.pop(key, None)

        print(
            "[InMemoryRedis.delete] "
            f"key={key}, existed={existed}"
        )
