from src.websocket.sender import WebSocketSender
from src.utils.logging import log


def handle_ping(event, payload):
    log("handle_ping", payload_keys=list(payload.keys()) if isinstance(payload, dict) else "n/a")

    websocket = WebSocketSender(event)
    websocket.send(action="pong")

    return {"statusCode": 200}
