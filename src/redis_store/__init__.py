from src.config.base import BaseConfig
from src.redis_store.session_store_redis import (
    WebSocketSessionStoreRedis,
)
from src.redis_store.session_store_memory import (
    WebSocketSessionStoreMemory,
)

session_store = (
    WebSocketSessionStoreRedis
    if BaseConfig.REDIS_ENABLED
    else WebSocketSessionStoreMemory
)
