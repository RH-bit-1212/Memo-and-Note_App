from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.sqlite import JSON
from datetime import datetime
from db import Base
from sqlalchemy.sql import func
from models.tag import Tag
from models.category import Category

# 中間テーブル（多対多）
memo_tags = Table(
    "memo_tags",
    Base.metadata,
    Column("memo_id", Integer, ForeignKey("memos.id"), primary_key=True),
    Column("tag_id", Integer, ForeignKey("tags.id"), primary_key=True),
    extend_existing=True  # ← 追加
)

class Memo(Base):
    __tablename__ = "memos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(400), nullable=False)
    content = Column(Text, nullable=True)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=True)
    file_paths = Column(JSON, nullable=True)   # 文字列リストをJSONで格納
    urls = Column(JSON, nullable=True)         # 文字列リストをJSONで格納
    important = Column(Integer, default=1)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    category = relationship("Category", back_populates="memos")
    tags = relationship("Tag", secondary=memo_tags, back_populates="memos")  # ← タグ配列
