from typing import Any, Dict
from src.utils.time import current_datetime_utc
from src.utils.logging import log


def build_ws_response(
    action: str,
    data: Dict[str, Any] | None = None,
) -> Dict[str, Any]:
    """
    Build a canonical WebSocket response envelope.
    """
    response = {
        "action": action,
        "data": data or {},
        "meta": {
            "timestamp": current_datetime_utc()
        },
    }

    log(
        "build_ws_response",
        action=action,
        data_keys=list((data or {}).keys())
    )
    return response
