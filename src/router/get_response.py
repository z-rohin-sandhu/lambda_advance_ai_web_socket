from src.websocket.sender import WebSocketSender
from src.redis_store import session_store

def handle_get_response(event, payload):
    websocket = WebSocketSender(event)

    session_id = payload.get("state_json_key")
    if not session_id:
        websocket.send(
            {
                "action": "error",
                "message": "state_json_key is required",
            }
        )
        return {"statusCode": 400}

    session_store.bind_session_to_connection(
        session_id=session_id,
        connection_id=websocket.connection_id,
    )

    websocket.send(
        {
            "action": "ack",
            "message": "Session bound successfully",
            "session_id": session_id,
        }
    )

    return {"statusCode": 200}
