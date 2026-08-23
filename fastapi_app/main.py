# fastapi-app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from sqlalchemy.orm import Session
import os
from db import Base, engine, SessionLocal, get_db

# ===================================================
# Models（Base登録用）
# ===================================================
import models.user
import models.category
import models.tag
import models.memo

# ===================================================
# Routers
# ===================================================
from routers.auth import router as auth_router
from routers.category import router as category_router
from routers.tag import router as tag_router
from routers.memo import router as memo_router
from routers.admin import router as admin_router

# ===================================================
# 初期管理者作成
# ===================================================
from crud.user import (
    create_user,
    get_user_by_username,
)

from schemas.user import UserCreate


# ===================================================
# DB 初期化
# ===================================================
Base.metadata.create_all(bind=engine)


# ===================================================
# FastAPI
# ===================================================
app = FastAPI(
    docs_url=None,
    redoc_url=None,
    openapi_url=None
)


# ===================================================
# CORS
# ===================================================
origins = [
    "http://localhost:5173",
    "http://localhost:8080",
    "http://127.0.0.1:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ===================================================
# Router 登録
# ===================================================
app.include_router(auth_router)
app.include_router(category_router)
app.include_router(tag_router)
app.include_router(memo_router)
app.include_router(admin_router)


# ===================================================
# 初期 admin 作成
# ===================================================
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")

if not ADMIN_USERNAME or not ADMIN_PASSWORD:
    raise RuntimeError(
        "ADMIN_USERNAME or ADMIN_PASSWORD is not configured"
    )


def init_admin(db: Session):
    admin = get_user_by_username(db, ADMIN_USERNAME)

    if not admin:
        create_user(
            db,
            UserCreate(
                username=ADMIN_USERNAME,
                password=ADMIN_PASSWORD,
                role="admin"
            )
        )


@app.on_event("startup")
def startup_event():
    db = SessionLocal()

    try:
        init_admin(db)
    finally:
        db.close()


# ===================================================
# Vue 配信用
# ===================================================
app.mount(
    "/css",
    StaticFiles(directory="frontend/dist/css"),
    name="css"
)

app.mount(
    "/js",
    StaticFiles(directory="frontend/dist/js"),
    name="js"
)

app.mount(
    "/img",
    StaticFiles(directory="frontend/dist/img"),
    name="img"
)


@app.get("/{full_path:path}")
async def serve_vue(full_path: str):
    return FileResponse("frontend/dist/index.html")
