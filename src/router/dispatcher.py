from src.router.connect import handle_connect
from src.router.disconnect import handle_disconnect
from src.router.ping import handle_ping
from src.router.get_response import handle_get_response
from src.websocket.sender import WebSocketSender

import json
import traceback
from src.utils.logging import log


def dispatch(event, context):
    try:
        request_context = event.get("requestContext", {})
        route_key = request_context.get("routeKey")

        log("dispatcher route", route_key=route_key)

        if route_key == "$connect":
            handle_connect(event)
            return {"statusCode": 200}

        if route_key == "$disconnect":
            handle_disconnect(event)
            return {"statusCode": 200}

        # $default route
        body = event.get("body")
        if not body:
            log("dispatcher empty body")
            return {"statusCode": 200}

        payload = json.loads(body)
        action = payload.get("action")

        log("dispatcher action", action=action)

        if action == "ping":
            handle_ping(event, payload)
            return {"statusCode": 200}

        if action == "get_response":
            handle_get_response(event, payload)
            return {"statusCode": 200}

        # Unknown action — DO NOT throw
        websocket = WebSocketSender(event)
        websocket.send(action="error", data={
            "message": f"Unknown action: {action}"
        })

        return {"statusCode": 200}

    except Exception as exc:
        log("dispatcher unhandled error", level="ERROR", error=str(exc))
        log(traceback.format_exc(), level="ERROR")

        return {"statusCode": 200}
