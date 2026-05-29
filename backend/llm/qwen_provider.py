from .openai_provider import OpenAICompatibleProvider


class QwenProvider(OpenAICompatibleProvider):
    provider_name = "qwen"

    def __init__(
        self,
        api_key: str,
        base_url: str = "https://dashscope.aliyuncs.com/compatible-mode/v1",
        model: str = "qwen-plus",
    ):
        super().__init__(api_key=api_key, base_url=base_url, model=model)
