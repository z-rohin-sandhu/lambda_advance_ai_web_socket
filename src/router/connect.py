from src.redis_store import session_store
from src.utils.logging import log
from src.websocket.sender import WebSocketSender
from src.utils.constants import DEFAULT_WS_SUCCESS_RESPONSE
from src.auth.jwt import verify_jwt_token_ws, JWTAuthError



def handle_connect(event, payload):
    try:
        connection_id = event.get("requestContext", {}).get("connectionId")
        session_id = payload.get("state_json_key")

        params = event.get("queryStringParameters") or {}
        token = params.get("token")

        decoded_token = verify_jwt_token_ws(token)

        if not session_id or not connection_id:
            raise JWTAuthError("Missing session_id or connection_id")

        log("handle_connect", connection_id=connection_id, session_id=session_id, decoded_token=decoded_token)
        
        session_store.register_connection(connection_id=connection_id, session_id=session_id, decoded_token=decoded_token)

        websocket = WebSocketSender(event=event)

        websocket.send(action="connection_ack", data={
            "connectionId": connection_id,
            "status": "connected",
            "sessionId": session_id,
        })

        return DEFAULT_WS_SUCCESS_RESPONSE
    
    except JWTAuthError as exc:
        log(
            "connect auth failed",
            level="ERROR",
            connection_id=connection_id,
            error=str(exc),
        )
        
        raise Exception(f"Unauthorized: {str(exc)}")
    
    except Exception as exc:
        log(
            "connect unhandled error",
            level="ERROR",
            connection_id=connection_id,
            error=str(exc),
        )
        raise Exception(f"Something went wrong: {str(exc)}")