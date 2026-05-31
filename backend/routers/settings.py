from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

from database.db import get_ai_setting, save_ai_setting

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
    try:
        from openai import OpenAI
    except Exception:
        return _bad("后端缺少 openai 依赖，无法测试 OpenAI Compatible 模型")

    api_key = _setting(settings, provider, "key")
    base_url = _setting(settings, provider, "baseUrl")
    model = _setting(settings, provider, "model")

    if provider != "local" and not api_key:
        return _bad("请先填写 API Key")
    if not base_url:
        return _bad("请先填写 Base URL")
    if not model:
        return _bad("请先填写模型名")

    try:
        client = OpenAI(api_key=api_key or "local", base_url=base_url, timeout=10)
        client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": "ping"}],
            max_tokens=1,
            temperature=0,
        )
    except Exception as exc:
        return _bad(f"{provider} 连接失败：{exc}")

    return {
        "code": 200,
        "message": f"{provider} 连接成功",
        "data": {"provider": provider, "model": model, "mode": "openai-compatible"},
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
    if provider in {"openai", "qwen", "deepseek", "local"}:
        return _test_openai_compatible(provider, settings)
    if provider == "gemini":
        return _test_gemini(settings)
    if provider == "ollama":
        return _test_ollama(settings)
    return _bad("不支持的模型服务商")
