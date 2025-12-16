from src.redis_store.session_store import unregister_connection

def handle_disconnect(event):
    connection_id = event["requestContext"]["connectionId"]
    unregister_connection(connection_id)

    return {
        "statusCode": 200,
        "body": "WebSocket disconnected and cleaned successfully",
    }
