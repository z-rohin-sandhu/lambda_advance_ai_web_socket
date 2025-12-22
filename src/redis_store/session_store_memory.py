from src.constants.redis_keys import (
    WS_SESSION_CONNECTION_KEY,
    DEFAULT_CONNECTION_TTL_SECONDS
)
from src.redis_store.memory_store import InMemoryRedis
from src.utils.time import current_timestamp
from src.utils.logging import log


class WebSocketSessionStoreMemory:
    @staticmethod
    def register_connection(connection_id: str, session_id: str, decoded_token: dict) -> None:
        log("session_store.memory.register_connection", connection_id=connection_id)

        InMemoryRedis.set(
            key=WS_SESSION_CONNECTION_KEY.format(session_id=session_id, connection_id=connection_id),
            value={
                "connection_id": connection_id,
                "session_id": session_id,
                "decoded_token": decoded_token,
                "updated_at": current_timestamp(),
            },
            ttl_seconds=DEFAULT_CONNECTION_TTL_SECONDS,
        )

    @staticmethod
    def unregister_connection(connection_id: str, session_id: str) -> None:
        log("session_store.memory.unregister_connection", connection_id=connection_id)

        InMemoryRedis.delete(
            WS_SESSION_CONNECTION_KEY.format(session_id=session_id, connection_id=connection_id)
        )

    @staticmethod
    def get_connection_for_session(session_id: str, connection_id: str):
        log("session_store.memory.get_connection_for_session", session_id=session_id, connection_id=connection_id)

        raw_data = InMemoryRedis.get(
            WS_SESSION_CONNECTION_KEY.format(session_id=session_id, connection_id=connection_id)
        )

        found = bool(raw_data)
        log("session_store.memory.get_connection_for_session.result", found=found)

        return raw_data
