from src.websocket.sender import WebSocketSender
from src.utils.logging import log
from src.utils.constants import (
    WS_ACTION_CONNECTION_ACK,
    DEFAULT_WS_SUCCESS_RESPONSE,
)
from src.redis_store import session_store


def handle_ping(event, payload):
    try:
        connection_id = event.get("requestContext", {}).get("connectionId")
        session_id = payload.get("state_json_key")

        log(
            "handle_ping",
            connection_id=connection_id,
            session_id=session_id,
        )

        if not session_id:
            raise Exception("session_id is required")

        session_store.get_session(session_id=session_id)
            
        websocket = WebSocketSender(event)

        websocket.send(
            action=WS_ACTION_CONNECTION_ACK,
            data={
                "connectionId": connection_id,
                "status": "connected",
                "sessionId": session_id,
            },
        )

        return DEFAULT_WS_SUCCESS_RESPONSE
    
    except Exception as exc:
        log(
            "handle_ping unhandled error",
            level="ERROR",
            connection_id=connection_id,
            session_id=session_id,
            error=str(exc),
        )
        raise Exception(f"handle_ping unhandled error: {str(exc)}")