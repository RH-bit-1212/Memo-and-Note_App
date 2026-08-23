from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from schemas.tag import TagResponse

class MemoBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=2000)
    content: Optional[str] = None
    category_id: Optional[int] = None
    file_paths: List[str] = Field(default_factory=list)
    urls: List[str] = Field(default_factory=list)
    important: int = 1
    tag_ids: List[int] = Field(default_factory=list)

class MemoCreate(MemoBase):
    pass

class MemoUpdate(MemoBase):
    pass

class MemoResponse(MemoBase):
    id: int
    user_id: int  # ← 追加
    created_at: datetime
    updated_at: datetime
    tags: List[TagResponse] = []

    model_config = {"from_attributes": True}
