from src.providers.llm.llm_factory import LLMStreamFactory
from src.services.resource_service import get_llm_resource_round_robin
from src.utils.logging import log


class AdvanceAIService:
    """
    Orchestration layer.
    NO streaming.
    NO WebSocket logic.
    """

    @staticmethod
    def fetch_advance_resources(
        brand_id: int,
        brand_settings_id: int,
        resource_type: str,
        bot_db=None,
    ) -> dict:
        """
        Returns ONE LLM resource using round-robin.
        Cached in Redis by existing infra.
        """
        log(
            "advance_ai_service.fetch_advance_resources",
            brand_id=brand_id,
            brand_settings_id=brand_settings_id,
        )
        

        resource = get_llm_resource_round_robin(
            brand_id=brand_id,
            brand_settings_id=brand_settings_id,
            resource_type=resource_type,
            bot_db=bot_db,
        )

        if not resource:
            raise RuntimeError("No LLM resource available")

        return resource

    @staticmethod
    def create_llm_stream(
        provider_name: str,
        resource: dict,
        payload: dict,
    ):
        """
        Factory method to return a streaming generator.
        """
        log(
            "advance_ai_service.create_llm_stream",
            provider=provider_name,
            model=resource.get("model_name"),
        )

        provider = LLMStreamFactory.create(
            provider_name=provider_name,
            resource=resource,
            payload=payload,
        )

        return provider.stream()
