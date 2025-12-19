import boto3
from src.websocket.response import build_ws_response
from src.utils.logging import log
from src.utils.json_utils import json_dumps

class WebSocketSender:
    def __init__(self, event: dict):
        self.connection_id = event.get("requestContext", {}).get("connectionId")
        self.domain_name = event.get("requestContext", {}).get("domainName")
        self.stage = event.get("requestContext", {}).get("stage")
        self.endpoint_url = f"https://{self.domain_name}/{self.stage}"

        log(
            "WebSocketSender initialized",
            f"connection_id={self.connection_id}, "
            f"domain_name={self.domain_name}, "
            f"stage={self.stage}, "
            f"endpoint_url={self.endpoint_url}"
        )

        self.client = boto3.client(
            "apigatewaymanagementapi",
            endpoint_url=self.endpoint_url,
        )

    def send(self, action: str, data: dict | None = None) -> None:
        response = build_ws_response(action=action, data=data)

        log(
            "WebSocketSender.send",
            connection_id=self.connection_id,
            action=action,
            response=response
        )

        self.client.post_to_connection(
            ConnectionId=self.connection_id,
            Data=json_dumps(response).encode("utf-8"),
        )
