from pydantic import BaseModel, Field
from datetime import datetime

class CategoryBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)
    description: str | None = None

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(CategoryBase):
    pass

class CategoryResponse(CategoryBase):
    id: int
    user_id: int  # ← 追加
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
