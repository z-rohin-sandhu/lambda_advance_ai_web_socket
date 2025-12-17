from src.redis_store import session_store


def handle_connect(event):
    connection_id = event["requestContext"]["connectionId"]
    session_store.register_connection(connection_id)

    return {
        "statusCode": 200,
        "body": "WebSocket connected and registered successfully",
    }
