from src.websocket.sender import WebSocketSender

def handle_ping(event, payload):
    websocket = WebSocketSender(event)
    websocket.send({"action": "pong"})
    return {"statusCode": 200, "message": "Pong"}
