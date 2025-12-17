import time
import threading

from src.websocket.stream import WebSocketStream
from src.utils.logging import log


def fake_stream_response(event):
    log("fake_stream_response invoked")

    def _run():
        try:
            stream = WebSocketStream(event)

            chunks = [
                "Hello",
                " this",
                " is",
                " a",
                " streamed",
                " response.",
            ]

            total_chunks = len(chunks)

            for index, chunk in enumerate(chunks):
                stream.send_chunk(
                    text=chunk,
                    is_last=(index == total_chunks - 1),
                )
                time.sleep(0.3)

            stream.complete()

        except Exception as exc:
            log(
                "fake_stream_response failed",
                level="ERROR",
                error=str(exc),
            )

    threading.Thread(target=_run, daemon=True).start()
