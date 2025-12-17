from src.redis_store import session_store


def handle_connect(event):
    connection_id = event["requestContext"]["connectionId"]

    print(f"[handle_connect] connection_id={connection_id}")

    session_store.register_connection(connection_id)

    return {"statusCode": 200}
