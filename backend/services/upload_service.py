import os
from typing import Iterable
from uuid import uuid4

from fastapi import UploadFile

from config import COVER_DIR, IMAGE_DIR, VIDEO_DIR, ensure_upload_dirs

IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".webp"}
VIDEO_EXTS = {".mp4", ".mov", ".avi", ".mkv"}


FOLDER_MAP = {
    "images": IMAGE_DIR,
    "videos": VIDEO_DIR,
    "covers": COVER_DIR,
}


class UploadError(ValueError):
    pass


def _safe_filename(filename: str) -> str:
    base = os.path.basename(filename)
    if not base:
        raise UploadError("文件名不能为空")
    return base


def _ensure_unique(target_dir: str, filename: str) -> str:
    path = os.path.join(target_dir, filename)
    if not os.path.exists(path):
        return filename
    name, ext = os.path.splitext(filename)
    return f"{name}-{uuid4().hex[:8]}{ext}"


def _read_in_chunks(upload: UploadFile, target_path: str, max_bytes: int) -> int:
    size = 0
    with open(target_path, "wb") as buffer:
        while True:
            chunk = upload.file.read(1024 * 1024)
            if not chunk:
                break
            size += len(chunk)
            if size > max_bytes:
                buffer.close()
                if os.path.exists(target_path):
                    os.remove(target_path)
                raise UploadError("文件过大")
            buffer.write(chunk)
    return size


def save_upload(
    file: UploadFile,
    folder_key: str,
    allowed_exts: Iterable[str],
    max_size_mb: int,
    file_type: str,
) -> dict:
    ensure_upload_dirs()

    filename = _safe_filename(file.filename or "")
    ext = os.path.splitext(filename)[1].lower()
    if ext not in set(allowed_exts):
        raise UploadError("文件格式不支持")

    target_dir = FOLDER_MAP[folder_key]
    safe_name = _ensure_unique(target_dir, filename)
    target_path = os.path.join(target_dir, safe_name)

    try:
        size = _read_in_chunks(file, target_path, max_size_mb * 1024 * 1024)
    finally:
        file.file.close()

    return {
        "file_name": safe_name,
        "file_url": f"/uploads/{folder_key}/{safe_name}",
        "file_type": file_type,
        "size": size,
    }
