from fastapi import APIRouter
from pydantic import BaseModel, Field

from database.db import get_ai_setting, save_ai_setting

router = APIRouter(prefix="/settings")


class LLMSettingRequest(BaseModel):
    provider: str = "openai"
    settings: dict = Field(default_factory=dict)


@router.get("/llm")
def get_llm():
    return {"code": 200, "data": get_ai_setting()}


@router.post("/llm")
def save_llm(payload: LLMSettingRequest):
    return {"code": 200, "message": "AI 设置已保存", "data": save_ai_setting(payload.provider, payload.settings)}
