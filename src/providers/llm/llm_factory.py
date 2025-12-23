from src.providers.llm.openai_provider import OpenAIStreamProvider
from src.utils.logging import log


class LLMStreamFactory:
    @staticmethod
    def create(provider_name: str, resource: dict, payload: dict):
        log("llm_factory.create", provider=provider_name)

        if provider_name == "openai":
            return OpenAIStreamProvider(resource, payload)

        raise ValueError(f"Unsupported LLM provider: {provider_name}")
