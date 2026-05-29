from .openai_provider import OpenAICompatibleProvider


class LocalProvider(OpenAICompatibleProvider):
    provider_name = "local"

    def __init__(self, base_url: str = "http://127.0.0.1:8000/v1", model: str = "local-model"):
        super().__init__(api_key="local", base_url=base_url, model=model)
