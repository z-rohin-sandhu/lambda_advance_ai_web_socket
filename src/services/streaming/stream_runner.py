import traceback
from typing import Dict

from src.websocket.stream import WebSocketStream
from src.services.advance_ai_service import AdvanceAIService
from src.utils.logging import log
from src.utils.constants import (
    WS_ACTION_RESPONSE_CHUNK,
    WS_ACTION_RESPONSE_COMPLETE,
    WS_ACTION_ERROR,
)


def run_stream(
    event: dict,
    payload: dict,
    session: dict,
) -> None:
    """
    Core streaming runner.

    This function:
    - Executes LLM streaming
    - Pushes chunks to WebSocket
    - Never raises
    """

    stream = WebSocketStream(event)

    try:
        log(
            "stream_runner.start",
            session_id=payload.get("state_json_key"),
            connection_id=stream.connection_id,
        )

        user_query = payload.get("query")
        if not user_query:
            stream.send(
                action=WS_ACTION_ERROR,
                data={
                    "error_code": "INVALID_REQUEST",
                    "error_message": "query is required",
                },
            )
            return

        decoded_token = session.get("decoded_token", {})
        brand_id = decoded_token.get("brand_id")
        brand_settings_id = decoded_token.get("brand_settings_id")

        if not brand_id or not brand_settings_id:
            stream.send(
                action=WS_ACTION_ERROR,
                data={
                    "error_code": "SESSION_INVALID",
                    "error_message": "Session context missing",
                },
            )
            return

        messages = [
            {
                "role": "system",
                "content": "You are a helpful AI assistant.",
            },
            {
                "role": "user",
                "content": user_query,
            },
        ]

        llm_payload: Dict = {
            "messages": messages,
        }

        resource = AdvanceAIService.fetch_advance_resources(
            brand_id=brand_id,
            brand_settings_id=brand_settings_id,
        )

        llm_stream = AdvanceAIService.create_llm_stream(
            provider_name="openai",
            resource=resource,
            payload=llm_payload,
        )

        full_reply = ""
        sequence_id = 0

        for chunk in llm_stream:
            full_reply += chunk

            stream.send(
                action=WS_ACTION_RESPONSE_CHUNK,
                data={
                    "bot_reply": chunk,
                    "sequence_id": sequence_id,
                    "audio": None,  # added later
                },
            )

            sequence_id += 1

        stream.send(
            action=WS_ACTION_RESPONSE_COMPLETE,
            data={
                "status": "success",
                "bot_reply": full_reply,
            },
        )

        log(
            "stream_runner.complete",
            session_id=payload.get("state_json_key"),
            total_chunks=sequence_id,
        )

    except Exception as exc:
        log(
            "stream_runner.failed",
            level="ERROR",
            error=str(exc),
        )
        log(traceback.format_exc(), level="ERROR")

        try:
            stream.send(
                action=WS_ACTION_ERROR,
                data={
                    "error_code": "STREAM_FAILED",
                    "error_message": "Failed while generating response",
                },
            )
        except Exception:
            pass
