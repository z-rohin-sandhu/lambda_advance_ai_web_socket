from src.router.connect import handle_connect
from src.router.disconnect import handle_disconnect
from src.router.ping import handle_ping
from src.router.get_response import handle_get_response
from src.utils.constants import (
    DEFAULT_WS_SUCCESS_RESPONSE,
    WS_ACTION_PING,
    WS_ACTION_GET_RESPONSE,
)
from src.utils.json_utils import json_loads
from src.utils.logging import log
import traceback


def dispatch(event, context):
    try:
        request_context = event.get("requestContext", {})
        route_key = request_context.get("routeKey")

        log("dispatcher route", route_key=route_key)

        # --- SYSTEM ROUTES ---
        if route_key == "$connect":
            return handle_connect(event)

        if route_key == "$disconnect":
            return handle_disconnect(event)

        # --- APPLICATION ROUTES ---
        body = event.get("body")
        if not body:
            log("dispatcher empty body")
            return DEFAULT_WS_SUCCESS_RESPONSE

        payload = json_loads(body)
        action = payload.get("action")

        log("dispatcher action", action=action)

        if action == WS_ACTION_PING:
            handle_ping(event, payload)

        elif action == WS_ACTION_GET_RESPONSE:
            handle_get_response(event, payload)

        else:
            log("dispatcher unknown action", action=action)


    except Exception as exc:
        log("dispatcher unhandled error", level="ERROR", error=str(exc))
        log(traceback.format_exc(), level="ERROR")
    
    return DEFAULT_WS_SUCCESS_RESPONSE
