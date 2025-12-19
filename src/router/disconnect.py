from src.redis_store import session_store
from src.utils.logging import log
from src.utils.constants import DEFAULT_WS_SUCCESS_RESPONSE

def handle_disconnect(event):
    connection_id = event["requestContext"]["connectionId"]
    log("handle_disconnect", connection_id=connection_id)

    session_store.unregister_connection(connection_id)

    return DEFAULT_WS_SUCCESS_RESPONSE
