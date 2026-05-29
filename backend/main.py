from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from config import UPLOAD_ROOT, ensure_upload_dirs
from database.db import init_db
from routers import account, auth, content, llm, publish, settings, upload

app = FastAPI(title="聚发舟 MultiPost AI", version="0.2.0")

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


app.include_router(content.router, prefix="/api")
app.include_router(upload.router, prefix="/api")
app.include_router(llm.router, prefix="/api")
app.include_router(publish.router, prefix="/api")
app.include_router(auth.router, prefix="/api")
app.include_router(account.router, prefix="/api")
app.include_router(settings.router, prefix="/api")

app.mount("/uploads", StaticFiles(directory=UPLOAD_ROOT), name="uploads")
