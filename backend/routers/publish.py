from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse

from database.db import get_record_detail, list_platform_contents, list_records
from models.schemas import PublishRequest
from services.publish_service import simulate_publish

router = APIRouter()


@router.post("/publish")
def publish(payload: PublishRequest):
    if not payload.task_id:
        return JSONResponse(
            status_code=400,
            content={"code": 400, "message": "task_id 不能为空", "data": None},
        )
    if not payload.platforms:
        return JSONResponse(
            status_code=400,
            content={"code": 400, "message": "请至少选择一个平台", "data": None},
        )

    contents = payload.contents or list_platform_contents(payload.task_id)
    if not contents:
        return JSONResponse(
            status_code=400,
            content={"code": 400, "message": "内容不存在", "data": None},
        )

    try:
        results = simulate_publish(
            task_id=payload.task_id,
            platforms=payload.platforms,
            contents=contents,
        )
    except Exception:
        return JSONResponse(
            status_code=500,
            content={"code": 500, "message": "发布失败", "data": None},
        )

    return {"code": 200, "message": "发布完成", "data": results}


@router.get("/records")
def records(limit: int = Query(50, ge=1, le=200)):
    return {"code": 200, "data": list_records(limit=limit)}


@router.get("/records/{record_id}")
def record_detail(record_id: int):
    detail = get_record_detail(record_id)
    if not detail:
        return JSONResponse(status_code=404, content={"code": 404, "message": "记录不存在"})
    return {"code": 200, "data": detail}
