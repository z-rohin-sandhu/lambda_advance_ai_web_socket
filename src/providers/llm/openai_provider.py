import openai
from src.utils.logging import log


class OpenAIStreamProvider:
    def __init__(self, resource: dict, payload: dict):
        self.api_key = resource["key"]
        self.endpoint = resource["endpoint"]
        self.model = resource["model_name"]
        self.payload = payload

        openai.api_key = self.api_key
        openai.api_base = self.endpoint

    def stream(self):
        log("openai_provider.stream.start", model=self.model)

        response = openai.ChatCompletion.create(
            engine=self.model,
            messages=self.payload["messages"],
            stream=True,
        )

        for chunk in response:
            delta = (
                chunk.get("choices", [{}])[0]
                .get("delta", {})
                .get("content")
            )

            if delta:
                yield delta
