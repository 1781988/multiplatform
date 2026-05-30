from .base_provider import BaseLLMProvider


class GeminiProvider(BaseLLMProvider):
    provider_name = "gemini"

    def __init__(self, api_key: str, model: str, temperature: float = 0.7, max_tokens: int | None = None):
        import google.generativeai as genai

        genai.configure(api_key=api_key)
        generation_config = {"temperature": temperature}
        if max_tokens:
            generation_config["max_output_tokens"] = max_tokens
        self.model = genai.GenerativeModel(model)
        self.generation_config = generation_config

    def generate(self, prompt: str, system_prompt: str = "") -> str:
        full_prompt = system_prompt + "\n" + prompt if system_prompt else prompt
        response = self.model.generate_content(full_prompt, generation_config=self.generation_config)
        return response.text or ""
