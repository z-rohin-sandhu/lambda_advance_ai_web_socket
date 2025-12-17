from src.config.env import EnvConfig
from src.constants.redis_keys import (
    WS_CONNECTION_KEY,
    WS_SESSION_KEY,
)
from src.redis_store.client import get_client
from src.utils.time import current_timestamp
from src.utils.json_utils import json_dumps, json_loads
from src.utils.logging import log


class WebSocketSessionStoreRedis:
    @staticmethod
    def register_connection(connection_id: str) -> None:
        log("session_store.redis.register_connection", connection_id=connection_id)

        redis_client = get_client()
        redis_client.setex(
            WS_CONNECTION_KEY.format(connection_id=connection_id),
            EnvConfig.REDIS_CONNECTION_TTL_SECONDS,
            json_dumps(
                {
                    "connection_id": connection_id,
                    "connected_at": current_timestamp(),
                }
            ),
        )

    @staticmethod
    def unregister_connection(connection_id: str) -> None:
        log("session_store.redis.unregister_connection", connection_id=connection_id)

        redis_client = get_client()
        redis_client.delete(
            WS_CONNECTION_KEY.format(connection_id=connection_id)
        )

    @staticmethod
    def bind_session_to_connection(
        session_id: str, connection_id: str
    ) -> None:
        log(
            "session_store.redis.bind_session_to_connection",
            session_id=session_id,
            connection_id=connection_id,
        )

        redis_client = get_client()
        redis_client.setex(
            WS_SESSION_KEY.format(session_id=session_id),
            EnvConfig.REDIS_SESSION_TTL_SECONDS_SECONDS,
            json_dumps(
                {
                    "connection_id": connection_id,
                    "updated_at": current_timestamp(),
                }
            ),
        )

    @staticmethod
    def get_connection_for_session(session_id: str):
        log("session_store.redis.get_connection_for_session", session_id=session_id)

        redis_client = get_client()
        raw_data = redis_client.get(
            WS_SESSION_KEY.format(session_id=session_id)
        )

        found = bool(raw_data)
        log("session_store.redis.get_connection_for_session.result", found=found)

        return json_loads(raw_data) if raw_data else None
