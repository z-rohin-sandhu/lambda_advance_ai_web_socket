import json
import boto3

class WebSocketSender:
    def __init__(self, event):
        ctx = event["requestContext"]
        self.connection_id = ctx["connectionId"]
        self.endpoint = f"https://{ctx['domainName']}/{ctx['stage']}"

        self.client = boto3.client(
            "apigatewaymanagementapi",
            endpoint_url=self.endpoint
        )

    def send(self, payload: dict):
        self.client.post_to_connection(
            ConnectionId=self.connection_id,
            Data=json.dumps(payload).encode("utf-8")
        )
