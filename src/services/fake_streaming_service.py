import time
from src.websocket.stream import WebSocketStream
from src.utils.logging import log


def fake_stream_response(event):
    log("fake_stream_response invoked")

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
        log("fake_stream_response chunk sent", chunk=chunk)
        time.sleep(0.3)

    log("fake_stream_response complete")
    stream.complete()
    log("fake_stream_response complete")
