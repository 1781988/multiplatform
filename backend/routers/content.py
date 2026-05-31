from fastapi import APIRouter
from fastapi.responses import JSONResponse

from database.db import create_platform_content, create_task, get_ai_setting
from models.schemas import AdaptRequest, ContentGenerateRequest, MediaFiles
from services.adapter_service import adapt_content
from services import llm_service
from services.llm_service import normalize_provider

router = APIRouter()


def _clean_tags(tags: list) -> list:
    return [str(tag).strip() for tag in tags if str(tag).strip()]


def _clean_media(media_files: MediaFiles | None, cover_fallback: str | None = None) -> MediaFiles:
    media = media_files or MediaFiles()
    images = [str(item).strip() for item in media.images if str(item).strip()]
    videos = [str(item).strip() for item in media.videos if str(item).strip()]
    cover = (media.cover or "").strip() or None
    if not cover and cover_fallback:
        cover = cover_fallback
    return MediaFiles(images=images, videos=videos, cover=cover)


def _handle_generate(payload: ContentGenerateRequest) -> dict | JSONResponse:
    title = payload.title.strip()
    content = payload.content.strip()
    tags = _clean_tags(payload.tags)

    if not title:
        return JSONResponse(
            status_code=400,
            content={"code": 400, "message": "标题不能为空", "data": None},
        )
    if not content:
        return JSONResponse(
            status_code=400,
            content={"code": 400, "message": "正文不能为空", "data": None},
        )
    if not payload.platforms:
        return JSONResponse(
            status_code=400,
            content={"code": 400, "message": "请至少选择一个平台", "data": None},
        )

    try:
        default_ai_settings = get_ai_setting() if payload.use_ai else {}
        provider = normalize_provider(payload.llm_provider or default_ai_settings.get("provider"))
        if payload.use_ai and not provider:
            provider = "openai"
        clean_media = _clean_media(payload.media_files)
        clean_payload = payload.model_copy(
            update={
                "title": title,
                "content": content,
                "tags": tags,
                "llm_provider": provider,
                "media_files": clean_media,
            }
        )
        task_id = create_task(
            title=title,
            content=content,
            tags=tags,
            platforms=payload.platforms,
            author=payload.author,
            use_ai=payload.use_ai or False,
            llm_provider=provider,
        )

        data = adapt_content(clean_payload)
        ai_message = llm_service.LAST_LLM_ERROR if payload.use_ai else ""

        for platform, payload_item in data.items():
            create_platform_content(task_id, platform, payload_item)
    except ValueError as exc:
        return JSONResponse(
            status_code=400,
            content={"code": 400, "message": str(exc), "data": None},
        )
    except Exception:
        return JSONResponse(
            status_code=500,
            content={"code": 500, "message": "生成失败", "data": None},
        )

    return {
        "code": 200,
        "message": ai_message or "生成成功",
        "task_id": task_id,
        "data": data,
        "ai_fallback": bool(ai_message),
    }


@router.post("/content/generate")
def generate(payload: ContentGenerateRequest):
    return _handle_generate(payload)


@router.post("/adapt")
def adapt(payload: AdaptRequest):
    cover_image = (payload.cover_image or "").strip() or None
    media_files = _clean_media(None, cover_image)
    converted = ContentGenerateRequest(
        title=payload.title,
        content=payload.content,
        tags=payload.tags,
        author=None,
        platforms=payload.platforms,
        use_ai=payload.use_ai or False,
        llm_provider=payload.llm_provider,
        media_files=media_files,
    )
    return _handle_generate(converted)
