from pydantic import BaseModel, Field
from datetime import datetime

class TagBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)
    color: str | None = None

class TagCreate(TagBase):
    pass

class TagUpdate(TagBase):
    pass

class TagResponse(TagBase):
    id: int
    user_id: int  # ← 追加
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
