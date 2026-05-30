from fastapi import APIRouter
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


@router.post("/llm/test")
def test_llm(payload: LLMTestRequest):
    provider = payload.provider.strip().lower()
    settings = payload.settings or {}
    supported = {"openai", "qwen", "gemini", "deepseek", "ollama", "local"}

    if provider not in supported:
        return {"code": 400, "message": "不支持的模型服务商"}

    api_key = settings.get(f"{provider}Key", "")
    base_url = settings.get(f"{provider}BaseUrl", "")
    model = settings.get(f"{provider}Model", "")

    if provider in {"openai", "qwen", "gemini", "deepseek"} and not api_key:
        return {"code": 400, "message": "请先填写 API Key"}
    if provider in {"openai", "qwen", "deepseek", "ollama", "local"} and not base_url:
        return {"code": 400, "message": "请先填写 Base URL"}
    if not model:
        return {"code": 400, "message": "请先填写模型名"}

    return {
        "code": 200,
        "message": "连接配置校验通过",
        "data": {
            "provider": provider,
            "model": model,
            "mode": "mock",
            "ready_for_real_api": True,
        },
    }
