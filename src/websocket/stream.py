from src.websocket.sender import WebSocketSender
from src.utils.logging import log


class WebSocketStream:
    """
    Transport adapter for streaming over WebSocket.
    """

    def __init__(self, event: dict):
        self.sender = WebSocketSender(event)
        self.connection_id = self.sender.connection_id

        log(
            "WebSocketStream.init",
            connection_id=self.connection_id,
        )

    def send(self, action: str, data: dict) -> None:
        """
        Send a streaming frame.
        """
        self.sender.send(action=action, data=data)
