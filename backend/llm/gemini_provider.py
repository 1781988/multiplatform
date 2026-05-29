from .base_provider import BaseLLMProvider


class GeminiProvider(BaseLLMProvider):
    provider_name = "gemini"

    def __init__(self, api_key: str, model: str):
        import google.generativeai as genai

        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model)

    def generate(self, prompt: str, system_prompt: str = "") -> str:
        full_prompt = system_prompt + "\n" + prompt if system_prompt else prompt
        response = self.model.generate_content(full_prompt)
        return response.text or ""
