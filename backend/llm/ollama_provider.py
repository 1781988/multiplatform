from .base_provider import BaseLLMProvider


class OllamaProvider(BaseLLMProvider):
    provider_name = "ollama"

    def __init__(self, base_url: str, model: str, temperature: float = 0.7, max_tokens: int | None = None):
        self.base_url = base_url.rstrip("/")
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens

    def generate(self, prompt: str, system_prompt: str = "") -> str:
        import requests

        full_prompt = system_prompt + "\n" + prompt if system_prompt else prompt
        options = {"temperature": self.temperature}
        if self.max_tokens:
            options["num_predict"] = self.max_tokens
        response = requests.post(
            f"{self.base_url}/api/generate",
            json={
                "model": self.model,
                "prompt": full_prompt,
                "stream": False,
                "options": options,
            },
            timeout=120,
        )
        response.raise_for_status()
        return response.json().get("response", "")
