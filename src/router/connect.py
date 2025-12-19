from src.redis_store import session_store
from src.utils.logging import log
from src.websocket.sender import WebSocketSender
from src.utils.constants import DEFAULT_WS_SUCCESS_RESPONSE


def handle_connect(event, payload):
    connection_id = event["requestContext"]["connectionId"]
    session_id = payload.get("state_json_key")

    if not session_id or not connection_id:
        log("handle_connect invalid payload", payload=payload)
        return {"statusCode": 400}

    log("handle_connect", connection_id=connection_id, session_id=session_id)
    
    session_store.register_connection(connection_id)
    session_store.bind_session_to_connection(session_id, connection_id)

    websocket = WebSocketSender(event)
    websocket.send(action="connection_ack", data={
        "connectionId": connection_id,
        "status": "connected",
        "sessionId": session_id,
    })

    return DEFAULT_WS_SUCCESS_RESPONSE