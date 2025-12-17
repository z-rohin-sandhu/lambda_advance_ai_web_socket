from src.constants.redis_keys import (
    WS_CONNECTION_KEY,
    WS_SESSION_KEY,
    DEFAULT_CONNECTION_TTL_SECONDS,
    DEFAULT_SESSION_TTL_SECONDS_SECONDS,
)
from src.redis_store.memory_store import InMemoryRedis
from src.utils.time import current_timestamp
from src.utils.logging import log


class WebSocketSessionStoreMemory:
    @staticmethod
    def register_connection(connection_id: str) -> None:
        log("session_store.memory.register_connection", connection_id=connection_id)

        InMemoryRedis.set(
            key=WS_CONNECTION_KEY.format(connection_id=connection_id),
            value={
                "connection_id": connection_id,
                "connected_at": current_timestamp(),
            },
            ttl_seconds=DEFAULT_CONNECTION_TTL_SECONDS,
        )

    @staticmethod
    def unregister_connection(connection_id: str) -> None:
        log("session_store.memory.unregister_connection", connection_id=connection_id)

        InMemoryRedis.delete(
            WS_CONNECTION_KEY.format(connection_id=connection_id)
        )

    @staticmethod
    def bind_session_to_connection(
        session_id: str, connection_id: str
    ) -> None:
        log(
            "session_store.memory.bind_session_to_connection",
            session_id=session_id,
            connection_id=connection_id,
        )

        InMemoryRedis.set(
            key=WS_SESSION_KEY.format(session_id=session_id),
            value={
                "connection_id": connection_id,
                "updated_at": current_timestamp(),
            },
            ttl_seconds=DEFAULT_SESSION_TTL_SECONDS_SECONDS,
        )

    @staticmethod
    def get_connection_for_session(session_id: str):
        log("session_store.memory.get_connection_for_session", session_id=session_id)

        raw_data = InMemoryRedis.get(
            WS_SESSION_KEY.format(session_id=session_id)
        )

        found = bool(raw_data)
        log("session_store.memory.get_connection_for_session.result", found=found)

        return raw_data
