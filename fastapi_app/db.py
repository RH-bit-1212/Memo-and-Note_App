# fastapi-app/db.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from pathlib import Path

"""
BASE_DIR = Path(__file__).resolve().parent.parent

DB_PATH = os.getenv(
    "DB_PATH",
    str(BASE_DIR / "data" / "memos.db")
)
"""


# 外部公開用
DB_PATH = os.getenv("DB_PATH", "/data/memos.db")

# ★ 追加：ディレクトリ作成
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

SQLALCHEMY_DATABASE_URL = f"sqlite:///{DB_PATH}"


# エンジン作成
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},  # SQLite 用おまじない
)

# セッション作成
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base クラス
Base = declarative_base()

# DB セッションを提供する関数（FastAPI の Depends で使用）
def get_db():
    """FastAPI の Depends で利用する DB セッション供給関数"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
