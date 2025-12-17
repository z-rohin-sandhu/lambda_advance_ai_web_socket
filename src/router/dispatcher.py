from src.router.connect import handle_connect
from src.router.disconnect import handle_disconnect
from src.router.ping import handle_ping
from src.router.get_response import handle_get_response
from src.websocket.sender import WebSocketSender

import json
import traceback


def dispatch(event, context):
    try:
        request_context = event.get("requestContext", {})
        route_key = request_context.get("routeKey")

        print(f"[dispatcher] route_key={route_key}")

        if route_key == "$connect":
            handle_connect(event)
            return {"statusCode": 200}

        if route_key == "$disconnect":
            handle_disconnect(event)
            return {"statusCode": 200}

        # $default route
        body = event.get("body")
        if not body:
            print("[dispatcher] empty body")
            return {"statusCode": 200}

        payload = json.loads(body)
        action = payload.get("action")

        print(f"[dispatcher] action={action}")

        if action == "ping":
            handle_ping(event, payload)
            return {"statusCode": 200}

        if action == "get_response":
            handle_get_response(event, payload)
            return {"statusCode": 200}

        # Unknown action — DO NOT throw
        websocket = WebSocketSender(event)
        websocket.send({
            "action": "error",
            "message": f"Unknown action: {action}"
        })

        return {"statusCode": 200}

    except Exception as exc:
        # ABSOLUTELY CRITICAL: swallow exception
        print("[dispatcher] UNHANDLED ERROR")
        print(traceback.format_exc())

        try:
            websocket = WebSocketSender(event)
            websocket.send({
                "action": "error",
                "message": "Internal server error"
            })
        except Exception:
            # Even this must not crash Lambda
            pass

        return {"statusCode": 200}
