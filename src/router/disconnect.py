from src.redis_store import session_store

def handle_disconnect(event):
    connection_id = event["requestContext"]["connectionId"]
    session_store.unregister_connection(connection_id)

    return {
        "statusCode": 200,
        "body": "WebSocket disconnected and cleaned successfully",
    }
