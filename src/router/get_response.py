import time
from src.websocket.sender import WebSocketSender
from src.websocket.stream import WebSocketStream
from src.redis_store import session_store
from src.utils.logging import log
import traceback


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

        stream = WebSocketStream(event)

        chunks = ["Hello", " this", " is", " a", " streamed", " response"]

        for chunk in chunks:
            stream.send_chunk(
                text=chunk,
                audio=None,
                is_last=False,
            )
            time.sleep(0.3)

        # Logical end of THIS GPT response
        stream.complete()

    except Exception as exc:
        log("get_response failed", level="ERROR", error=str(exc))
        log(traceback.format_exc(), level="ERROR")

    # WebSocket remains OPEN
    return {"statusCode": 200}
