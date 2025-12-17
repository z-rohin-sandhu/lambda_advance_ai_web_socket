from src.websocket.sender import WebSocketSender
from src.utils.logging import log


class WebSocketStream:
    def __init__(self, event):
        self.websocket = WebSocketSender(event)
        self.sequence = 0
        log("WebSocketStream initialized")

    def send_chunk(self, text: str, is_last: bool = False):
        payload = {
            "sequence": self.sequence,
            "text": text,
            "audio": None,
            "is_last": is_last,
        }

        log(
            "stream send_chunk",
            sequence=self.sequence,
            text_length=len(text),
            is_last=is_last,
        )

        self.websocket.send(
            action="response_chunk",
            data=payload,
        )

        self.sequence += 1

    def complete(self):
        log(
            "stream complete",
            total_chunks=self.sequence,
        )

        self.websocket.send(
            action="response_complete",
            data={
                "total_chunks": self.sequence,
            },
        )

    def error(self, message: str):
        log(
            "stream error",
            level="ERROR",
            message=message,
        )

        self.websocket.send(
            action="error",
            data={"message": message},
        )
