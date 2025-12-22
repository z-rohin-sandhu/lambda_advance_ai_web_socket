from src.redis_store import session_store
from src.utils.logging import log
from src.auth.jwt import verify_jwt_token_ws, JWTAuthError
from src.utils.constants import DEFAULT_WS_SUCCESS_RESPONSE


def handle_connect(event):
    try:
        request_context = event.get("requestContext", {})
        connection_id = request_context.get("connectionId")

        params = event.get("queryStringParameters") or {}
        token = params.get("token")
        session_id = params.get("state_json_key")

        log(
            "handle_connect invoked",
            connection_id=connection_id,
            session_id=session_id,
        )

        if not token or not session_id or not connection_id:
            log(
                "handle_connect missing params",
                level="ERROR",
                token_present=bool(token),
                session_id_present=bool(session_id),
            )
            raise Exception("Unauthorized")

        decoded_token = verify_jwt_token_ws(token)

        session_store.register_connection(
            connection_id=connection_id,
            session_id=session_id,
            decoded_token=decoded_token,
        )

        log(
            "handle_connect success",
            connection_id=connection_id,
            session_id=session_id,
            user_id=decoded_token.get("original_user", {}).get("user_id"),
        )

        return DEFAULT_WS_SUCCESS_RESPONSE

    except JWTAuthError as exc:
        log(
            "handle_connect auth failed",
            level="ERROR",
            connection_id=connection_id,
            error=str(exc),
        )
        raise Exception("Unauthorized")

    except Exception as exc:
        log(
            "handle_connect unhandled error",
            level="ERROR",
            connection_id=connection_id,
            error=str(exc),
        )
        raise Exception(f"handle_connect unhandled error: {str(exc)}")
