from src.websocket.sender import WebSocketSender

def handle_ping(event, payload):
    ws = WebSocketSender(event)
    ws.send({"action": "pong"})
    return {"statusCode": 200, "message": "Pong"}
