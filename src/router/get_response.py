from src.websocket.sender import WebSocketSender
from src.redis_store import session_store
from src.services.fake_streaming_service import fake_stream_response
from src.utils.logging import log


def handle_get_response(event, payload):
    log("handle_get_response invoked", payload=payload)

    websocket = WebSocketSender(event)
    connection_id = websocket.connection_id

    session_id = payload.get("state_json_key")

    if not session_id:
        websocket.send(
            action="error",
            data={"message": "state_json_key is required"},
        )
        return {"statusCode": 200}

    session_store.bind_session_to_connection(
        session_id=session_id,
        connection_id=connection_id,
    )

    websocket.send(
        action="ack",
        data={
            "message": "Session bound, streaming will start",
            "session_id": session_id,
        },
    )

    fake_stream_response(event)

    return {"statusCode": 200}
