from .openai_provider import OpenAICompatibleProvider


class LocalProvider(OpenAICompatibleProvider):
    provider_name = "local"

    def __init__(
        self,
        base_url: str = "http://127.0.0.1:8000/v1",
        model: str = "local-model",
        api_key: str = "local",
        temperature: float = 0.7,
        max_tokens: int | None = None,
    ):
        super().__init__(
            api_key=api_key or "local",
            base_url=base_url,
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
        )
