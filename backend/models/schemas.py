from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class MediaFiles(BaseModel):
    images: List[str] = Field(default_factory=list)
    videos: List[str] = Field(default_factory=list)
    cover: Optional[str] = None


class ContentGenerateRequest(BaseModel):
    title: str
    content: str
    tags: List[str] = Field(default_factory=list)
    author: Optional[str] = None
    platforms: List[str] = Field(default_factory=list)
    use_ai: Optional[bool] = False
    llm_provider: Optional[str] = None
    media_files: Optional[MediaFiles] = None


class AdaptRequest(BaseModel):
    title: str
    content: str
    tags: List[str] = Field(default_factory=list)
    cover_image: Optional[str] = None
    platforms: List[str] = Field(default_factory=list)
    use_ai: Optional[bool] = False
    llm_provider: Optional[str] = None


class PublishRequest(BaseModel):
    task_id: int
    platforms: List[str] = Field(default_factory=list)
    contents: Optional[Dict[str, Dict[str, Any]]] = None
