from fastapi import APIRouter, File, UploadFile
from fastapi.responses import JSONResponse

from database.db import create_media_file, list_materials
from services.upload_service import IMAGE_EXTS, VIDEO_EXTS, UploadError, save_upload

router = APIRouter(prefix="/upload")


def _persist_upload(data: dict) -> None:
    create_media_file(
        task_id=None,
        file_name=data["file_name"],
        file_url=data["file_url"],
        file_type=data["file_type"],
        file_size=data["size"],
    )


@router.post("/image")
def upload_image(file: UploadFile = File(...)):
    try:
        data = save_upload(
            file=file,
            folder_key="images",
            allowed_exts=IMAGE_EXTS,
            max_size_mb=10,
            file_type="image",
        )
        _persist_upload(data)
    except UploadError as exc:
        return JSONResponse(status_code=400, content={"code": 400, "message": str(exc)})
    except Exception:
        return JSONResponse(status_code=500, content={"code": 500, "message": "图片上传失败"})

    return {"code": 200, "message": "图片上传成功", "data": data}


@router.post("/video")
def upload_video(file: UploadFile = File(...)):
    try:
        data = save_upload(
            file=file,
            folder_key="videos",
            allowed_exts=VIDEO_EXTS,
            max_size_mb=500,
            file_type="video",
        )
        _persist_upload(data)
    except UploadError as exc:
        return JSONResponse(status_code=400, content={"code": 400, "message": str(exc)})
    except Exception:
        return JSONResponse(status_code=500, content={"code": 500, "message": "视频上传失败"})

    return {"code": 200, "message": "视频上传成功", "data": data}


@router.post("/cover")
def upload_cover(file: UploadFile = File(...)):
    try:
        data = save_upload(
            file=file,
            folder_key="covers",
            allowed_exts=IMAGE_EXTS,
            max_size_mb=10,
            file_type="cover",
        )
        _persist_upload(data)
    except UploadError as exc:
        return JSONResponse(status_code=400, content={"code": 400, "message": str(exc)})
    except Exception:
        return JSONResponse(status_code=500, content={"code": 500, "message": "封面上传失败"})

    return {"code": 200, "message": "封面上传成功", "data": data}


@router.get("/materials")
def materials():
    return {"code": 200, "data": list_materials()}
