import json
import logging
from typing import Optional

from llm.factory import AVAILABLE_PROVIDERS, get_llm_provider
from models.schemas import ContentGenerateRequest

logger = logging.getLogger(__name__)
LAST_LLM_ERROR = ""

SYSTEM_PROMPT = """你是一个多平台内容运营助手。请根据用户提供的原始内容，将其改写为适合 {platform} 平台发布的内容。
要求：
1. 保留原始主题和核心信息。
2. 符合目标平台的表达风格。
3. 生成 title、content、tags、summary、description、category 等字段。
4. 不要编造原文没有的重要事实。
5. 只输出 JSON，不要输出解释文字。
"""

PLATFORM_STYLES = {
    "wechat": "公众号风格：正式、结构化、有导语和总结，适合深度阅读。标题可突出系统性指南。",
    "zhihu": "知乎风格：问题导向、分析型、分点说明、带有专业标签。标题适合用问句。",
    "bilibili": "B站风格：视频标题吸引人，简介简洁有力，并给出合适分区。",
    "xiaohongshu": "小红书风格：口语化、种草语气、短句分行，并带话题标签。",
}


def list_providers() -> list:
    return AVAILABLE_PROVIDERS


def normalize_provider(provider: Optional[str]) -> Optional[str]:
    if provider is None:
        return None
    normalized = provider.strip().lower()
    if not normalized:
        return None
    if normalized not in AVAILABLE_PROVIDERS:
        raise ValueError(f"不支持的模型服务商: {provider}")
    return normalized


def generate_ai_content(payload: ContentGenerateRequest) -> Optional[dict]:
    global LAST_LLM_ERROR
    LAST_LLM_ERROR = ""
    provider_name = (payload.llm_provider or "").strip().lower()
    if not provider_name:
        return None

    llm = get_llm_provider(provider_name)
    if llm is None:
        LAST_LLM_ERROR = f"{provider_name} 未配置或 API Key 为空，已使用本地模板。"
        logger.warning("LLM provider %s unavailable, falling back to rule templates", provider_name)
        return None

    tags_text = ", ".join(payload.tags) if payload.tags else "无"
    user_prompt = f"""原始标题：{payload.title}

原始正文：{payload.content}

原始标签：{tags_text}"""

    results = {}
    for platform in payload.platforms:
        style = PLATFORM_STYLES.get(platform, "")
        system = SYSTEM_PROMPT.replace("{platform}", platform)
        if style:
            system += "\n" + style

        try:
            raw = llm.generate(prompt=user_prompt, system_prompt=system)
            results[platform] = _parse_ai_response(raw, platform, payload)
        except Exception as exc:
            LAST_LLM_ERROR = f"{provider_name} 调用失败：{exc}"
            logger.warning("AI rewrite failed for %s: %s; using rule fallback", platform, exc)
            continue

    return results if results else None


def _parse_ai_response(raw: str, platform: str, payload: ContentGenerateRequest) -> dict:
    media = payload.media_files.model_dump() if payload.media_files else {}
    images = list(media.get("images", []))
    videos = list(media.get("videos", []))
    cover = media.get("cover")

    try:
        cleaned = raw.strip()
        if cleaned.startswith("```"):
            cleaned = cleaned.split("\n", 1)[-1]
            if cleaned.endswith("```"):
                cleaned = cleaned[:-3]
        data = json.loads(cleaned)
    except (json.JSONDecodeError, AttributeError):
        data = {}

    title = str(data.get("title", "")).strip() or payload.title
    content = str(data.get("content", "")).strip()
    description = str(data.get("description", "")).strip()
    summary = str(data.get("summary", "")).strip()
    category = str(data.get("category", "")).strip()
    tags = _normalize_tags(data.get("tags", [])) or list(payload.tags)

    if not content and not description:
        content = payload.content

    if platform == "bilibili":
        return {
            "platform": platform,
            "title": title,
            "description": description or content,
            "content": description or content,
            "category": category or "知识",
            "tags": tags,
            "video": videos[0] if videos else "",
            "videos": videos,
            "images": images,
            "cover": cover,
        }

    result = {
        "platform": platform,
        "title": title,
        "content": content,
        "tags": tags,
        "images": images,
        "videos": videos,
        "cover": cover,
    }
    if summary:
        result["summary"] = summary
    if platform == "xiaohongshu" and videos:
        result["video"] = videos[0]
    return result


def _normalize_tags(tags) -> list:
    if not isinstance(tags, list):
        return []
    result = []
    for tag in tags:
        text = str(tag).strip().lstrip("#")
        if text:
            result.append(text)
    return result
