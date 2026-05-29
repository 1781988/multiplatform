import os
from typing import Optional

from dotenv import load_dotenv

from .base_provider import BaseLLMProvider
from .deepseek_provider import DeepSeekProvider
from .gemini_provider import GeminiProvider
from .local_provider import LocalProvider
from .ollama_provider import OllamaProvider
from .openai_provider import OpenAICompatibleProvider
from .qwen_provider import QwenProvider

load_dotenv()

PROVIDER_BUILDERS = {
    "openai": OpenAICompatibleProvider,
    "gemini": GeminiProvider,
    "qwen": QwenProvider,
    "deepseek": DeepSeekProvider,
    "ollama": OllamaProvider,
    "local": LocalProvider,
}

AVAILABLE_PROVIDERS = list(PROVIDER_BUILDERS.keys())


def load_provider_from_env(provider: str) -> Optional[BaseLLMProvider]:
    key = provider.strip().lower()
    if key not in PROVIDER_BUILDERS:
        return None

    try:
        if key == "openai":
            api_key = os.getenv("OPENAI_API_KEY", "")
            base_url = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
            model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
            if not api_key:
                return None
            return OpenAICompatibleProvider(api_key=api_key, base_url=base_url, model=model)

        if key == "gemini":
            api_key = os.getenv("GEMINI_API_KEY", "")
            model = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
            if not api_key:
                return None
            return GeminiProvider(api_key=api_key, model=model)

        if key == "qwen":
            api_key = os.getenv("QWEN_API_KEY", "")
            base_url = os.getenv("QWEN_BASE_URL", "https://dashscope.aliyuncs.com/compatible-mode/v1")
            model = os.getenv("QWEN_MODEL", "qwen-plus")
            if not api_key:
                return None
            return QwenProvider(api_key=api_key, base_url=base_url, model=model)

        if key == "deepseek":
            api_key = os.getenv("DEEPSEEK_API_KEY", "")
            base_url = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com")
            model = os.getenv("DEEPSEEK_MODEL", "deepseek-chat")
            if not api_key:
                return None
            return DeepSeekProvider(api_key=api_key, base_url=base_url, model=model)

        if key == "ollama":
            base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
            model = os.getenv("OLLAMA_MODEL", "qwen2.5:7b")
            return OllamaProvider(base_url=base_url, model=model)

        if key == "local":
            base_url = os.getenv("LOCAL_LLM_BASE_URL", "http://127.0.0.1:8000/v1")
            model = os.getenv("LOCAL_LLM_MODEL", "local-model")
            return LocalProvider(base_url=base_url, model=model)

    except Exception:
        return None

    return None


def get_llm_provider(provider: str) -> Optional[BaseLLMProvider]:
    return load_provider_from_env(provider)
