from src.websocket.sender import WebSocketSender


def handle_ping(event, payload):
    print(f"[handle_ping] payload={payload}")

    websocket = WebSocketSender(event)
    websocket.send(action="pong")

    return {"statusCode": 200}
