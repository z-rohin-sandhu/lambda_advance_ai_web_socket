from src.config.env import EnvConfig
from src.constants.redis_keys import (
  WS_SESSION_CONNECTION_KEY
)
from src.redis_store.client import get_client
from src.utils.time import current_timestamp
from src.utils.json_utils import json_dumps
from src.utils.logging import log


class WebSocketSessionStoreRedis:
    @staticmethod
    def register_connection(connection_id: str, session_id: str, decoded_token: dict) -> None:
        log("session_store.redis.register_connection", connection_id=connection_id)

        redis_client = get_client()
        redis_client.setex(
            WS_SESSION_CONNECTION_KEY.format(session_id=session_id, connection_id=connection_id),
            EnvConfig.REDIS_CONNECTION_TTL_SECONDS,
            json_dumps(
                {
                    "connection_id": connection_id,
                    "session_id": session_id,
                    "decoded_token": decoded_token,
                    "updated_at": current_timestamp(),
                }
            ),
        )

    @staticmethod
    def unregister_connection(connection_id: str, session_id: str) -> None:
        log("session_store.redis.unregister_connection", connection_id=connection_id)

        redis_client = get_client()
        redis_client.delete(
            WS_SESSION_CONNECTION_KEY.format(session_id=session_id, connection_id=connection_id)
        )

    @staticmethod
    def get_connection_for_session(session_id: str, connection_id: str):
        log("session_store.redis.get_connection_for_session", session_id=session_id, connection_id=connection_id)

        redis_client = get_client()
        raw_data = redis_client.get(WS_SESSION_CONNECTION_KEY.format(session_id=session_id, connection_id=connection_id))

        found = bool(raw_data)
        log("session_store.redis.get_connection_for_session.result", found=found)

        return raw_data if found else None
