import threading
import traceback

from src.services.streaming.stream_runner import run_stream
from src.utils.logging import log


def start_streaming_job(
    event: dict,
    payload: dict,
    session: dict,
) -> None:
    """
    Fire-and-forget streaming job.

    Responsibilities:
    - Spawn background thread
    - Pass validated inputs to stream runner
    - NEVER block Lambda
    - NEVER raise
    """

    log(
        "streaming_service.start_streaming_job",
        session_id=session.get("session_id"),
        connection_id=session.get("connection_id"),
    )

    def _runner():
        try:
            run_stream(
                event=event,
                payload=payload,
                session=session,
            )
        except Exception as exc:
            # Absolutely must not crash the process
            log(
                "streaming_service.run_stream.failed",
                level="ERROR",
                error=str(exc),
            )
            log(traceback.format_exc(), level="ERROR")

    thread = threading.Thread(
        target=_runner,
        daemon=True,  # critical: Lambda must not wait
    )
    thread.start()
