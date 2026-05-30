import os
from typing import Optional

from dotenv import load_dotenv

from database.db import get_ai_setting

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


def _setting_value(settings: dict, provider: str, field: str, default=None):
    key = f"{provider}{field[0].upper()}{field[1:]}"
    value = settings.get(key)
    return default if value in (None, "") else value


def _float_value(value, default: float = 0.7) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _int_value(value, default: int | None = None) -> int | None:
    try:
        number = int(value)
    except (TypeError, ValueError):
        return default
    return number if number > 0 else default


def load_provider_from_settings(provider: str, settings: dict | None = None) -> Optional[BaseLLMProvider]:
    key = provider.strip().lower()
    if key not in PROVIDER_BUILDERS:
        return None

    settings = settings or get_ai_setting()
    if not settings:
        return None

    temperature = _float_value(_setting_value(settings, key, "temperature", 0.7))
    max_tokens = _int_value(_setting_value(settings, key, "maxTokens"))

    try:
        if key == "openai":
            api_key = _setting_value(settings, key, "key", "")
            base_url = _setting_value(settings, key, "baseUrl", "https://api.openai.com/v1")
            model = _setting_value(settings, key, "model", "gpt-4o-mini")
            if not api_key:
                return None
            return OpenAICompatibleProvider(api_key, base_url, model, temperature, max_tokens)

        if key == "gemini":
            api_key = _setting_value(settings, key, "key", "")
            model = _setting_value(settings, key, "model", "gemini-1.5-flash")
            if not api_key:
                return None
            return GeminiProvider(api_key, model, temperature, max_tokens)

        if key == "qwen":
            api_key = _setting_value(settings, key, "key", "")
            base_url = _setting_value(settings, key, "baseUrl", "https://dashscope.aliyuncs.com/compatible-mode/v1")
            model = _setting_value(settings, key, "model", "qwen-plus")
            if not api_key:
                return None
            return QwenProvider(api_key, base_url, model, temperature, max_tokens)

        if key == "deepseek":
            api_key = _setting_value(settings, key, "key", "")
            base_url = _setting_value(settings, key, "baseUrl", "https://api.deepseek.com")
            model = _setting_value(settings, key, "model", "deepseek-chat")
            if not api_key:
                return None
            return DeepSeekProvider(api_key, base_url, model, temperature, max_tokens)

        if key == "ollama":
            base_url = _setting_value(settings, key, "baseUrl", "http://localhost:11434")
            model = _setting_value(settings, key, "model", "qwen2.5:7b")
            return OllamaProvider(base_url, model, temperature, max_tokens)

        if key == "local":
            api_key = _setting_value(settings, key, "key", "local")
            base_url = _setting_value(settings, key, "baseUrl", "http://127.0.0.1:8000/v1")
            model = _setting_value(settings, key, "model", "local-model")
            return LocalProvider(base_url, model, api_key, temperature, max_tokens)

    except Exception:
        return None

    return None


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
    return load_provider_from_settings(provider) or load_provider_from_env(provider)
