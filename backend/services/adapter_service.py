from adapters.registry import ADAPTER_REGISTRY
from models.schemas import ContentGenerateRequest
from services.llm_service import generate_ai_content


def adapt_content(payload: ContentGenerateRequest) -> dict:
    data = payload.model_dump()
    ai_result = None
    if payload.use_ai:
        ai_result = generate_ai_content(payload)
    if ai_result:
        return ai_result
    results = {}
    seen = set()

    for platform in payload.platforms:
        if platform in seen:
            continue
        seen.add(platform)
        adapter = ADAPTER_REGISTRY.get(platform)
        if not adapter:
            raise ValueError(f"unsupported platform: {platform}")
        results[platform] = adapter.adapt(data)

    return results
