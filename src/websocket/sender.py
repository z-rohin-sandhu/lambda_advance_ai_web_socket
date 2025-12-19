import json
import boto3
from src.websocket.response import build_ws_response
from src.utils.logging import log



class WebSocketSender:
    def __init__(self, event: dict):
        self.connection_id = event["requestContext"]["connectionId"]
        domain_name = event["requestContext"]["domainName"]
        stage = event["requestContext"]["stage"]

        endpoint_url = f"https://{domain_name}/{stage}"

        log(
            "[WebSocketSender] init "
            f"connection_id={self.connection_id}, "
            f"endpoint={endpoint_url}"
        )

        self.client = boto3.client(
            "apigatewaymanagementapi",
            endpoint_url=endpoint_url,
        )

    def send(self, action: str, data: dict | None = None) -> None:
        payload = build_ws_response(action=action, data=data)

        log(
            "WebSocketSender.send",
            connection_id=self.connection_id,
            action=action,
        )

        self.client.post_to_connection(
            ConnectionId=self.connection_id,
            Data=json.dumps(payload).encode("utf-8"),
        )
