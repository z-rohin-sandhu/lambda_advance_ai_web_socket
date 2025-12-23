from abc import ABC, abstractmethod
from typing import Dict, Iterator, Any

from src.utils.logging import log


class BaseLLMStreamProvider(ABC):
    """
    Abstract base class for ALL LLM streaming providers.

    Guarantees:
    - Streaming is incremental
    - Order is preserved
    - Provider is stateless per request
    """

    def __init__(
        self,
        session: Dict[str, Any],
        payload: Dict[str, Any],
    ) -> None:
        """
        Initialize provider with session + request payload.

        session:
            - Decoded JWT
            - User / account / brand info
            - Retrieved from Redis

        payload:
            - Incoming WebSocket message
            - Includes query, story_type, voice, etc.
        """
        self.session = session
        self.payload = payload

        self.session_id = payload.get("state_json_key")

        log(
            "LLM provider initialized",
            provider=self.__class__.__name__,
            session_id=self.session_id,
        )

    @abstractmethod
    def stream(self) -> Iterator[Dict[str, Any]]:
        """
        Stream tokens/chunks from the LLM.

        MUST yield dicts with this shape:

        {
            "text": "partial response"
        }

        Rules:
        - Yield order MUST be preserved
        - Empty yields MUST be skipped
        - Exceptions MUST propagate upward
        """
        raise NotImplementedError

    @abstractmethod
    def get_model_name(self) -> str:
        """
        Return the model identifier used for this request.
        (Useful for logging, analytics, billing)
        """
        raise NotImplementedError
