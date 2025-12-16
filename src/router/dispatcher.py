from src.router.connect import handle_connect
from src.router.disconnect import handle_disconnect
from src.router.ping import handle_ping
from src.router.get_response import handle_get_response

import json


def dispatch(event, context):
    try:
        route_key = event["requestContext"]["routeKey"]

        if route_key == "$connect":
            return handle_connect(event)

        if route_key == "$disconnect":
            return handle_disconnect(event)

        # $default
        body = event.get("body")
        if not body:
            return {"statusCode": 200}

        payload = json.loads(body)
        action = payload.get("action")

        if action == "ping":
            return handle_ping(event, payload)

        if action == "get_response":
            return handle_get_response(event, payload)

        return {"statusCode": 200}
    
    except Exception as e:
        print(e)
        return {"statusCode": 500, "body": "Internal Server Error", "error": str(e)}