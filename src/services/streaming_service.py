import threading
from typing import Dict, Any

from src.websocket.stream import WebSocketStream
from src.services.llm.llm_factory import LLMStreamFactory
from src.services.tts.tts_factory import TTSFactory
from src.utils.logging import log
from src.utils.constants import (
    WS_ACTION_RESPONSE_CHUNK,
    WS_ACTION_RESPONSE_COMPLETE,
    WS_ACTION_ERROR,
)


def start_streaming_job(
    event: dict,
    payload: Dict[str, Any],
    session: Dict[str, Any],
) -> None:
    """
    Entry point for AI streaming.

    This function MUST:
    - Return immediately
    - Spawn background thread
    - Never block Lambda execution
    """

    log(
        "start_streaming_job invoked",
        session_id=payload.get("state_json_key"),
    )

    thread = threading.Thread(
        target=_run_stream,
        kwargs={
            "event": event,
            "payload": payload,
            "session": session,
        },
        daemon=True,
    )
    thread.start()


def _run_stream(
    event: dict,
    payload: Dict[str, Any],
    session: Dict[str, Any],
) -> None:
    """
    Streaming execution layer.

    This is where:
    - LLM streaming happens
    - Optional TTS synthesis happens
    - WebSocket chunks are pushed
    """

    session_id = payload.get("state_json_key")

    log(
        "stream execution started",
        session_id=session_id,
    )

    try:
        stream = WebSocketStream(event)

        # 1️⃣ Resolve providers
        llm_provider = LLMStreamFactory.get_provider(
            provider_name=payload.get("llm_provider", "openai"),
            session=session,
            payload=payload,
        )

        tts_provider = None
        if payload.get("story_type") == "audio":
            tts_provider = TTSFactory.get_provider(
                provider_name=payload.get("tts_provider", "deepgram"),
                voice_id=payload.get("voice_id"),
                session=session,
            )

        # 2️⃣ Stream from LLM
        sequence_id = 0
        full_text = ""

        for llm_chunk in llm_provider.stream():
            text_chunk = llm_chunk.get("text")
            if not text_chunk:
                continue

            full_text += text_chunk

            audio_base64 = None
            if tts_provider:
                audio_base64 = tts_provider.synthesize(text_chunk)

            stream.send_chunk(
                action=WS_ACTION_RESPONSE_CHUNK,
                data={
                    "bot_reply": text_chunk,
                    "sequence_id": sequence_id,
                    "audio": audio_base64,
                },
            )

            sequence_id += 1

        # 3️⃣ Final message
        stream.send(
            action=WS_ACTION_RESPONSE_COMPLETE,
            data={
                "status": "success",
                "bot_reply": full_text,
            },
        )

        log(
            "stream execution completed",
            session_id=session_id,
            total_chunks=sequence_id,
        )

    except Exception as exc:
        log(
            "stream execution failed",
            level="ERROR",
            session_id=session_id,
            error=str(exc),
        )

        try:
            stream.send(
                action=WS_ACTION_ERROR,
                data={
                    "error_code": "STREAMING_FAILED",
                    "error_message": "Streaming failed. Please retry.",
                },
            )
        except Exception:
            # Socket may already be gone — swallow
            pass
