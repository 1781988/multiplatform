from .base_provider import BaseLLMProvider


class OpenAICompatibleProvider(BaseLLMProvider):
    provider_name = "openai"

    def __init__(
        self,
        api_key: str,
        base_url: str,
        model: str,
        temperature: float = 0.7,
        max_tokens: int | None = None,
    ):
        self.api_key = api_key
        self.base_url = _normalize_base_url(base_url)
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens

    def generate(self, prompt: str, system_prompt: str = "") -> str:
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        kwargs = {
            "model": self.model,
            "messages": messages,
            "temperature": self.temperature,
        }
        if self.max_tokens:
            kwargs["max_tokens"] = self.max_tokens

        import requests

        response = requests.post(
            f"{self.base_url}/chat/completions",
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            json=kwargs,
            timeout=90,
        )
        try:
            payload = response.json()
        except ValueError:
            payload = {"error": {"message": response.text}}
        if response.status_code >= 400:
            message = payload.get("error", {}).get("message") or response.text
            raise RuntimeError(f"HTTP {response.status_code}: {message}")
        return payload.get("choices", [{}])[0].get("message", {}).get("content") or ""


def _normalize_base_url(base_url: str) -> str:
    value = (base_url or "").rstrip("/")
    if value in {"https://api.deepseek.com", "https://api.siliconflow.cn"}:
        return f"{value}/v1"
    return value
