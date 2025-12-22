import jwt
from src.utils.logging import log
from src.config.base import BaseConfig
from src.utils.time import current_timestamp_utc
from src.utils.utils import check_token_blacklisted_status


class JWTAuthError(Exception):
    """Raised when JWT validation fails"""


def verify_jwt_token_ws(token: str) -> dict:
    """
    Verify JWT token for WebSocket $connect.
    Returns decoded payload on success.
    Raises JWTAuthError on failure.
    """

    if not token:
        log("verify_jwt_token_ws missing token")
        raise JWTAuthError("Missing token")

    # Blacklist check
    if check_token_blacklisted_status(token=token):
        raise JWTAuthError("Token blacklisted")

    try:
        payload = jwt.decode(
            token,
            key=BaseConfig.SECRET_KEY,
            algorithms=[BaseConfig.JWT_ALGORITHM],
        )
        log("verify_jwt_token_ws decoded payload", payload=payload)

    except jwt.ExpiredSignatureError:
        log("verify_jwt_token_ws token expired")
        raise JWTAuthError("Token expired")

    except jwt.InvalidTokenError:
        log("verify_jwt_token_ws invalid token")
        raise JWTAuthError("Invalid token")

    # Mandatory claims
    if not payload.get("exp"):
        log("verify_jwt_token_ws missing exp claim")
        raise JWTAuthError("Missing exp claim")

    if not payload.get("original_user") or not payload["original_user"].get("user_id"):
        raise JWTAuthError("Missing user_id")

    # Exp check (extra safety)
    now = current_timestamp_utc()
    if payload.get("exp", 0) <= now:
        log("verify_jwt_token_ws token expired")
        raise JWTAuthError("Token expired")

    log("verify_jwt_token_ws success", payload=payload)
    return payload
