from src.websocket.sender import WebSocketSender
from src.redis_store.session_store import bind_session_to_connection

def handle_get_response(event, payload):
    websocket_sender = WebSocketSender(event)

    session_id = payload.get("state_json_key")
    if not session_id:
        websocket_sender.send(
            {
                "action": "error",
                "message": "state_json_key is required",
            }
        )
        return {"statusCode": 400}

    bind_session_to_connection(
        session_id=session_id,
        connection_id=websocket_sender.connection_id,
    )

    websocket_sender.send(
        {
            "action": "ack",
            "message": "Session bound successfully",
            "session_id": session_id,
        }
    )

    return {"statusCode": 200}
