from fastapi import APIRouter

from services.llm_service import list_providers

router = APIRouter(prefix="/llm")


@router.get("/providers")
def providers():
    return {"code": 200, "data": list_providers()}
