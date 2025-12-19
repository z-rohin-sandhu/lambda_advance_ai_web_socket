import time
from src.websocket.sender import WebSocketSender
from src.services.fake_streaming_service import fake_stream_response
import traceback
from src.redis_store import session_store
from src.utils.logging import log


def handle_get_response(event, payload):
    websocket = WebSocketSender(event)

    try:
        session_id = payload.get("state_json_key")
        if not session_id:
            websocket.send({
                "action": "error",
                "message": "state_json_key is required",
            })
            return {"statusCode": 200}

        session_store.bind_session_to_connection(
            session_id=session_id,
            connection_id=websocket.connection_id,
        )

        websocket.send({
            "action": "ack",
            "data": {
                "message": "Session bound, streaming will start",
                "session_id": session_id,
            },
        })

        fake_stream_response(event)

    except Exception as exc:
        log("get_response failed", level="ERROR", error=str(exc))
        log(traceback.format_exc(), level="ERROR")

    # WebSocket remains OPEN
    return {"statusCode": 200}
