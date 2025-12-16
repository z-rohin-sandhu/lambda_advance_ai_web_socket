from src.redis_store.session_store import register_connection

def handle_connect(event):
    connection_id = event["requestContext"]["connectionId"]
    register_connection(connection_id)

    return {
        "statusCode": 200,
        "body": "WebSocket connected and registered successfully",
    }
