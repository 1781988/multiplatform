from adapters.registry import ADAPTER_REGISTRY
from models.schemas import ContentGenerateRequest
from services.llm_service import generate_ai_content


def adapt_content(payload: ContentGenerateRequest) -> dict:
    data = payload.model_dump()
    results = {}
    seen = set()

    if payload.use_ai:
        results.update(generate_ai_content(payload) or {})

    for platform in payload.platforms:
        if platform in seen:
            continue
        seen.add(platform)
        if platform in results:
            continue
        adapter = ADAPTER_REGISTRY.get(platform)
        if not adapter:
            raise ValueError(f"unsupported platform: {platform}")
        results[platform] = adapter.adapt(data)

    return results
