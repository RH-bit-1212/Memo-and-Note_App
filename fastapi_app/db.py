# fastapi-app/db.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# SQLite データベース URL
SQLALCHEMY_DATABASE_URL = "sqlite:///./memos.db"

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
