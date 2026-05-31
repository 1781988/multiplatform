from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

from database.db import get_ai_setting, save_ai_setting
from llm.openai_provider import _normalize_base_url

router = APIRouter(prefix="/settings")


class LLMSettingRequest(BaseModel):
    provider: str = "openai"
    settings: dict = Field(default_factory=dict)


class LLMTestRequest(BaseModel):
    provider: str = "openai"
    settings: dict = Field(default_factory=dict)


@router.get("/llm")
def get_llm():
    return {"code": 200, "data": get_ai_setting()}


@router.post("/llm")
def save_llm(payload: LLMSettingRequest):
    return {"code": 200, "message": "AI 设置已保存", "data": save_ai_setting(payload.provider, payload.settings)}


def _setting(settings: dict, provider: str, name: str, default: str = "") -> str:
    key = f"{provider}{name[0].upper()}{name[1:]}"
    return str(settings.get(key) or default).strip()


def _bad(message: str):
    return JSONResponse(status_code=400, content={"code": 400, "message": message, "data": None})


def _test_openai_compatible(provider: str, settings: dict):
    api_key = _setting(settings, provider, "key")
    base_url = _setting(settings, provider, "baseUrl")
    model = _setting(settings, provider, "model")

    if provider not in {"local"} and not api_key:
        return _bad("请先填写 API Key")
    if not base_url:
        return _bad("请先填写 Base URL")
    if not model:
        return _bad("请先填写模型名")

    try:
        import requests

        url = f"{_normalize_base_url(base_url)}/chat/completions"
        response = requests.post(
            url,
            headers={
                "Authorization": f"Bearer {api_key or 'local'}",
                "Content-Type": "application/json",
            },
            json={
                "model": model,
                "messages": [{"role": "user", "content": "ping"}],
                "max_tokens": 1,
                "temperature": 0,
            },
            timeout=30,
        )
        try:
            data = response.json()
        except ValueError:
            data = {"error": {"message": response.text}}
        if response.status_code >= 400:
            message = data.get("error", {}).get("message") or response.text
            return _bad(f"{provider} 连接失败：HTTP {response.status_code}: {message}")
    except Exception as exc:
        return _bad(f"{provider} 连接失败：{exc}")

    return {
        "code": 200,
        "message": f"{provider} 连接成功",
        "data": {"provider": provider, "model": model, "mode": "openai-compatible", "url": url},
    }


def _test_gemini(settings: dict):
    api_key = _setting(settings, "gemini", "key")
    model = _setting(settings, "gemini", "model")
    if not api_key:
        return _bad("请先填写 API Key")
    if not model:
        return _bad("请先填写模型名")

    try:
        import google.generativeai as genai

        genai.configure(api_key=api_key)
        gemini_model = genai.GenerativeModel(model)
        gemini_model.generate_content("ping", generation_config={"max_output_tokens": 1})
    except Exception as exc:
        return _bad(f"Gemini 连接失败：{exc}")

    return {"code": 200, "message": "Gemini 连接成功", "data": {"provider": "gemini", "model": model}}


def _test_ollama(settings: dict):
    base_url = _setting(settings, "ollama", "baseUrl", "http://localhost:11434").rstrip("/")
    model = _setting(settings, "ollama", "model")
    if not base_url:
        return _bad("请先填写 Base URL")
    if not model:
        return _bad("请先填写模型名")

    try:
        import requests

        response = requests.get(f"{base_url}/api/tags", timeout=5)
        response.raise_for_status()
        models = [item.get("name") for item in response.json().get("models", [])]
    except Exception as exc:
        return _bad(f"Ollama 连接失败：{exc}")

    if models and model not in models:
        return _bad(f"Ollama 服务可用，但未找到模型 {model}")

    return {"code": 200, "message": "Ollama 连接成功", "data": {"provider": "ollama", "model": model}}


@router.post("/llm/test")
def test_llm(payload: LLMTestRequest):
    provider = payload.provider.strip().lower()
    settings = payload.settings or {}
    save_ai_setting(provider, settings)
    if provider in {"openai", "qwen", "deepseek", "local"}:
        return _test_openai_compatible(provider, settings)
    if provider == "gemini":
        return _test_gemini(settings)
    if provider == "ollama":
        return _test_ollama(settings)
    return _bad("不支持的模型服务商")


@router.post("/llm-test")
def test_llm_alias(payload: LLMTestRequest):
    return test_llm(payload)


@router.get("/llm/debug")
def debug_llm():
    settings = get_ai_setting()
    provider = str(settings.get("provider") or "").lower()
    if not provider:
        return {"code": 200, "data": {"configured": False, "message": "尚未保存默认模型配置"}}
    base_url = _setting(settings, provider, "baseUrl")
    return {
        "code": 200,
        "data": {
            "configured": True,
            "provider": provider,
            "model": _setting(settings, provider, "model"),
            "has_key": bool(_setting(settings, provider, "key")) or provider in {"ollama", "local"},
            "base_url": base_url,
            "request_url": f"{_normalize_base_url(base_url)}/chat/completions" if base_url else "",
        },
    }
