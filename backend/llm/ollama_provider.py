from .base_provider import BaseLLMProvider


class OllamaProvider(BaseLLMProvider):
    provider_name = "ollama"

    def __init__(self, base_url: str, model: str):
        self.base_url = base_url.rstrip("/")
        self.model = model

    def generate(self, prompt: str, system_prompt: str = "") -> str:
        import requests

        full_prompt = system_prompt + "\n" + prompt if system_prompt else prompt
        response = requests.post(
            f"{self.base_url}/api/generate",
            json={
                "model": self.model,
                "prompt": full_prompt,
                "stream": False,
            },
            timeout=120,
        )
        response.raise_for_status()
        return response.json().get("response", "")
