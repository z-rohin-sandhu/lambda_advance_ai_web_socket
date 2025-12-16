from src.websocket.sender import WebSocketSender

def handle_get_response(event, payload):
    ws = WebSocketSender(event)

    ws.send({
        "action": "ack",
        "message": "get_response received, processing will start soon"
    })

    return {
        "statusCode": 200,
        "body": "get_response acknowledged"
    }
