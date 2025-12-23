from src.websocket.sender import WebSocketSender
from src.redis_store import session_store
from src.services.streaming_service import start_streaming_job
from src.utils.logging import log
from src.utils.constants import (
    DEFAULT_WS_SUCCESS_RESPONSE,
    WS_ACTION_ERROR,
)


def handle_get_response(event, payload):
    """
    Trigger AI response streaming over WebSocket.

    Responsibilities:
    - Validate payload
    - Validate session existence
    - Fire streaming job (non-blocking)
    - NEVER close socket
    - NEVER send ACK here
    """

    log("handle_get_response invoked", payload_keys=list(payload.keys()))

    websocket = WebSocketSender(event)

    try:
        session_id = payload.get("state_json_key")
        if not session_id:
            websocket.send(
                action=WS_ACTION_ERROR,
                data={
                    "error_code": "INVALID_REQUEST",
                    "error_message": "state_json_key is required",
                },
            )
            return DEFAULT_WS_SUCCESS_RESPONSE

        session = session_store.get_session(session_id)
        if not session:
            websocket.send(
                action=WS_ACTION_ERROR,
                data={
                    "error_code": "SESSION_NOT_FOUND",
                    "error_message": "Session expired or invalid. Please reconnect.",
                },
            )
            return DEFAULT_WS_SUCCESS_RESPONSE

        start_streaming_job(
            event=event,
            payload=payload,
            session=session,
        )

        log(
            "get_response streaming triggered",
            session_id=session_id,
            connection_id=websocket.connection_id,
        )

    except Exception as exc:
        log(
            "get_response failed",
            level="ERROR",
            error=str(exc),
        )

        websocket.send(
            action=WS_ACTION_ERROR,
            data={
                "error_code": "GENERATION_FAILED",
                "error_message": "Failed while generating response",
            },
        )

    return DEFAULT_WS_SUCCESS_RESPONSE
