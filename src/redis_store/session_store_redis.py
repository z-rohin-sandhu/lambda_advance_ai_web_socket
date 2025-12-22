from src.config.env import EnvConfig
from src.constants.redis_keys import (
  WS_SESSION_KEY
)
from src.redis_store.client import get_client
from src.utils.time import current_timestamp
from src.utils.json_utils import json_dumps, json_loads
from src.utils.logging import log


class WebSocketSessionStoreRedis:
    @staticmethod
    def register_connection(
        connection_id: str,
        session_id: str,
        decoded_token: dict,
    ) -> None:
        log(
            "session_store.redis.register_connection",
            connection_id=connection_id,
            session_id=session_id,
        )

        redis_client = get_client()

        redis_client.setex(
            WS_SESSION_KEY.format(session_id=session_id),
            EnvConfig.REDIS_CONNECTION_TTL_SECONDS,
            json_dumps(
                {
                    "connection_id": connection_id,
                    "decoded_token": decoded_token,
                    "connected_at": current_timestamp(),
                }
            ),
        )

    @staticmethod
    def remove_session(session_id: str) -> None:
        log("session_store.redis.remove_session", session_id=session_id)
        redis_client = get_client()
        redis_client.delete(WS_SESSION_KEY.format(session_id=session_id))

    @staticmethod
    def get_session(session_id: str):
        redis_client = get_client()
        raw = redis_client.get(WS_SESSION_KEY.format(session_id=session_id))
        return json_loads(raw) if raw else None
