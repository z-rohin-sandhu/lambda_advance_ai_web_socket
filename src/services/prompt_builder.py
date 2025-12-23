from typing import Dict, List
from src.utils.logging import log


def build_prompt(payload: dict, session: dict) -> Dict:
    """
    Build LLM prompt payload.
    This is intentionally simple for now.
    """

    user_query = payload.get("query")

    log(
        "prompt_builder.build",
        query_length=len(user_query) if user_query else 0,
    )

    messages: List[Dict] = [
        {
            "role": "system",
            "content": "You are a helpful AI assistant.",
        },
        {
            "role": "user",
            "content": user_query,
        },
    ]

    return {
        "messages": messages
    }
