from src.websocket.sender import WebSocketSender
from src.services.fake_streaming_service import fake_stream_response
from src.redis_store import session_store
from src.utils.logging import log
import traceback


def handle_get_response(event, payload):
    websocket = WebSocketSender(event)

    try:
        session_id = payload.get("state_json_key")
        if not session_id:
            websocket.send(
                action="error",
                data={"message": "state_json_key is required"},
            )
            return {"statusCode": 200}

        session_store.bind_session_to_connection(
            session_id=session_id,
            connection_id=websocket.connection_id,
        )

        websocket.send(
            action="ack",
            data={
                "message": "Session bound, streaming will start",
                "session_id": session_id,
            },
        )

        fake_stream_response(event)

        log("get_response complete")

    except Exception as exc:
        log("get_response failed", level="ERROR", error=str(exc))
        log(traceback.format_exc(), level="ERROR")
        websocket.send(action="error", data={
            "message": f"Failed while generating response: {str(exc)}",
        })  

    return {"statusCode": 200}
