from src.websocket.sender import WebSocketSender
from src.redis_store import session_store


def handle_get_response(event, payload):
    print(f"[handle_get_response] payload={payload}")

    websocket = WebSocketSender(event)
    connection_id = websocket.connection_id

    session_id = payload.get("state_json_key")

    if not session_id:
        print("[handle_get_response] missing state_json_key")

        websocket.send(
            action="error",
            data={
                "message": "state_json_key is required"
            },
        )

        # IMPORTANT: never return 4xx / 5xx for WebSocket
        return {"statusCode": 200}

    print(
        "[handle_get_response] binding session "
        f"session_id={session_id} -> connection_id={connection_id}"
    )

    session_store.bind_session_to_connection(
        session_id=session_id,
        connection_id=connection_id,
    )

    websocket.send(
        action="ack",
        data={
            "message": "Session bound successfully",
            "session_id": session_id,
        },
    )

    return {"statusCode": 200}
