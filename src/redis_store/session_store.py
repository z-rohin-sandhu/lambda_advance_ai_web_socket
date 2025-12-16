from operator import ge
from src.redis_store.client import get_client
from src.config.env import EnvConfig
from src.constants.redis_keys import (
    WS_CONNECTION_KEY,
    WS_SESSION_KEY,
)
from src.utils.time import current_timestamp
from src.utils.json_utils import json_dumps, json_loads


def register_connection(connection_id: str) -> None:
    print(f"[session_store.register_connection] connection_id={connection_id}")
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


def unregister_connection(connection_id: str) -> None:
    print(f"[session_store.unregister_connection] connection_id={connection_id}")
    redis_client = get_redis_client()
    redis_client.delete(
        WS_CONNECTION_KEY.format(connection_id=connection_id)
    )


def bind_session_to_connection(
    session_id: str, connection_id: str
) -> None:
    print(
        "[session_store.bind_session_to_connection] "
        f"session_id={session_id}, connection_id={connection_id}"
    )
    redis_client = get_redis_client()

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


def get_connection_for_session(session_id: str):
    print(f"[session_store.get_connection_for_session] session_id={session_id}")
    redis_client = get_redis_client()

    raw_data = redis_client.get(
        WS_SESSION_KEY.format(session_id=session_id)
    )
    print(
        "[session_store.get_connection_for_session] "
        f"found={bool(raw_data)}"
    )
    return json_loads(raw_data) if raw_data else None
