from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from config import UPLOAD_ROOT, ensure_upload_dirs
from database.db import init_db
from routers import account, auth, content, llm, publish, settings, upload

app = FastAPI(title="聚舟 MultiPost AI", version="0.2.0")

ensure_upload_dirs()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5173", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup() -> None:
    init_db()
    ensure_upload_dirs()


@app.get("/api/health")
def health() -> dict:
    return {"status": "ok"}


@app.get("/api/materials")
def materials_alias() -> dict:
    from database.db import list_materials

    return {"code": 200, "data": list_materials()}


@app.delete("/api/materials/{material_id}")
def delete_material_alias(material_id: int):
    import os

    from database.db import delete_material

    material = delete_material(material_id)
    if not material:
        return JSONResponse(status_code=404, content={"code": 404, "message": "素材不存在"})

    file_url = material.get("file_url") or ""
    relative_path = file_url.lstrip("/").replace("/", os.sep)
    if relative_path.startswith(f"uploads{os.sep}"):
        file_path = os.path.abspath(os.path.join(os.path.dirname(UPLOAD_ROOT), relative_path))
        upload_root = os.path.abspath(UPLOAD_ROOT)
        if file_path.startswith(upload_root) and os.path.exists(file_path):
            try:
                os.remove(file_path)
            except OSError:
                pass

    return {"code": 200, "message": "素材已删除", "data": material}


app.include_router(content.router, prefix="/api")
app.include_router(upload.router, prefix="/api")
app.include_router(llm.router, prefix="/api")
app.include_router(publish.router, prefix="/api")
app.include_router(auth.router, prefix="/api")
app.include_router(account.router, prefix="/api")
app.include_router(settings.router, prefix="/api")

app.mount("/uploads", StaticFiles(directory=UPLOAD_ROOT), name="uploads")
