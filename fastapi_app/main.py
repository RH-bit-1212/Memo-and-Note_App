from fastapi import FastAPI, Depends, HTTPException
from fastapi import Header
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from jose import jwt, JWTError

from db import Base, engine, get_db

# ===================================================
# CRUD
# ===================================================
from crud.user import (
    create_user,
    authenticate_user,
    get_users,
    get_user,
    update_user,
    delete_user,
    get_user_by_username,
)
from crud.category import (
    get_categories,
    get_category,
    create_category,
    update_category,
    delete_category,
)
from crud.tag import (
    get_tags,
    get_tag,
    create_tag,
    update_tag,
    delete_tag,
)
from crud.memo import (
    get_memos,
    get_memo,
    create_memo,
    update_memo,
    delete_memo,
)

# ===================================================
# Schemas
# ===================================================
from schemas.user import UserCreate, UserLogin, UserResponse
from schemas.category import CategoryCreate, CategoryUpdate, CategoryResponse
from schemas.tag import TagCreate, TagUpdate, TagResponse
from schemas.memo import MemoCreate, MemoUpdate, MemoResponse

# ===================================================
# Models（Base 登録）
# ===================================================
import models.user
import models.category
import models.tag
import models.memo

# ===================================================
# DB 初期化
# ===================================================
Base.metadata.create_all(bind=engine)

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
# JWT 設定
# ===================================================
SECRET_KEY = "TEST_SECRET_KEY"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24    #60 分 × 24 時間 = 1440分間

# ===================================================
# 初期 admin 作成
# ===================================================
#def init_admin(db: Session):
#    admin = get_user_by_username(db, "admin")
#    if not admin:
#        create_user(db, UserCreate(username="admin", password="admin123", role="admin"))

#@app.on_event("startup")
#def startup_event():
#    db = next(get_db())
#    init_admin(db)

# ===================================================
# JWT デコード
# ===================================================
def decode_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if not username:
            raise HTTPException(status_code=401, detail="Invalid token payload")
        return username
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

# ===================================================
# 認証 Dependencies
# ===================================================
def get_current_user(authorization: str = Header(...), db: Session = Depends(get_db)):
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization header")
    token = authorization.split(" ")[1]
    username = decode_token(token)
    user = get_user_by_username(db, username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

def get_current_admin(authorization: str = Header(...), db: Session = Depends(get_db)):
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization header")
    token = authorization.split(" ")[1]
    username = decode_token(token)
    admin = get_user_by_username(db, username)
    if not admin:
        raise HTTPException(status_code=404, detail="Admin not found")
    if admin.role != "admin":
        raise HTTPException(status_code=403, detail="Admin only")
    return admin

# ===================================================
# 認証 API
# ===================================================
@app.post("/login")
def login(data: UserLogin, db: Session = Depends(get_db)):
    user = authenticate_user(db, data.username, data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    token = jwt.encode({"sub": user.username, "role": user.role, "exp": expire}, SECRET_KEY, algorithm=ALGORITHM)
    return {"access_token": token}

# ===================================================
# カテゴリ CRUD（ユーザー制約）
# ===================================================
@app.get("/categories", response_model=list[CategoryResponse])
def read_categories(user=Depends(get_current_user), db: Session = Depends(get_db)):
    return get_categories(db, user.id)

@app.get("/categories/{category_id}", response_model=CategoryResponse)
def read_category(category_id: int, user=Depends(get_current_user), db: Session = Depends(get_db)):
    category = get_category(db, category_id, user.id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

@app.post("/categories", response_model=CategoryResponse)
def create_category_endpoint(category: CategoryCreate, user=Depends(get_current_user), db: Session = Depends(get_db)):
    return create_category(db, category, user.id)

@app.put("/categories/{category_id}", response_model=CategoryResponse)
def update_category_endpoint(category_id: int, category: CategoryUpdate, user=Depends(get_current_user), db: Session = Depends(get_db)):
    updated = update_category(db, category_id, category, user.id)
    if not updated:
        raise HTTPException(status_code=404, detail="Category not found")
    return updated

@app.delete("/categories/{category_id}")
def delete_category_endpoint(category_id: int, user=Depends(get_current_user), db: Session = Depends(get_db)):
    ok = delete_category(db, category_id, user.id)
    if not ok:
        raise HTTPException(status_code=404, detail="Category not found")
    return {"result": "ok"}

# ===================================================
# タグ CRUD（ユーザー制約）
# ===================================================
@app.get("/tags", response_model=list[TagResponse])
def read_tags(user=Depends(get_current_user), db: Session = Depends(get_db)):
    return get_tags(db, user.id)

@app.get("/tags/{tag_id}", response_model=TagResponse)
def read_tag(tag_id: int, user=Depends(get_current_user), db: Session = Depends(get_db)):
    tag = get_tag(db, tag_id, user.id)
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    return tag

@app.post("/tags", response_model=TagResponse)
def create_tag_endpoint(tag: TagCreate, user=Depends(get_current_user), db: Session = Depends(get_db)):
    return create_tag(db, tag, user.id)

@app.put("/tags/{tag_id}", response_model=TagResponse)
def update_tag_endpoint(tag_id: int, tag: TagUpdate, user=Depends(get_current_user), db: Session = Depends(get_db)):
    updated = update_tag(db, tag_id, tag, user.id)
    if not updated:
        raise HTTPException(status_code=404, detail="Tag not found")
    return updated

@app.delete("/tags/{tag_id}")
def delete_tag_endpoint(tag_id: int, user=Depends(get_current_user), db: Session = Depends(get_db)):
    ok = delete_tag(db, tag_id, user.id)
    if not ok:
        raise HTTPException(status_code=404, detail="Tag not found")
    return {"result": "ok"}

# ===================================================
# メモ CRUD（ユーザー制約）
# ===================================================
@app.get("/memos", response_model=list[MemoResponse])
def read_memos(user=Depends(get_current_user), db: Session = Depends(get_db)):
    return get_memos(db, user.id)

@app.get("/memos/{memo_id}", response_model=MemoResponse)
def read_memo(memo_id: int, user=Depends(get_current_user), db: Session = Depends(get_db)):
    memo = get_memo(db, memo_id, user.id)
    if not memo:
        raise HTTPException(status_code=404, detail="Memo not found")
    return memo

@app.post("/memos", response_model=MemoResponse)
def create_memo_endpoint(memo: MemoCreate, user=Depends(get_current_user), db: Session = Depends(get_db)):
    return create_memo(db, memo, user.id)

@app.put("/memos/{memo_id}", response_model=MemoResponse)
def update_memo_endpoint(memo_id: int, memo: MemoUpdate, user=Depends(get_current_user), db: Session = Depends(get_db)):
    updated = update_memo(db, memo_id, memo, user.id)
    if not updated:
        raise HTTPException(status_code=404, detail="Memo not found")
    return updated

@app.delete("/memos/{memo_id}")
def delete_memo_endpoint(memo_id: int, user=Depends(get_current_user), db: Session = Depends(get_db)):
    ok = delete_memo(db, memo_id, user.id)
    if not ok:
        raise HTTPException(status_code=404, detail="Memo not found")
    return {"result": "ok"}

# ===================================================
# ユーザー CRUD（管理者用）
# ===================================================
@app.get("/admin/users", response_model=list[UserResponse])
def admin_read_users(admin=Depends(get_current_admin), db: Session = Depends(get_db)):
    return get_users(db)

@app.get("/admin/users/{user_id}", response_model=UserResponse)
def admin_read_user(user_id: int, admin=Depends(get_current_admin), db: Session = Depends(get_db)):
    user = get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.post("/admin/users", response_model=UserResponse)
def admin_create_user(user: UserCreate, admin=Depends(get_current_admin), db: Session = Depends(get_db)):
    return create_user(db, user)

@app.put("/admin/users/{user_id}", response_model=UserResponse)
def admin_update_user(user_id: int, data: UserCreate, admin=Depends(get_current_admin), db: Session = Depends(get_db)):
    updated = update_user(db, user_id, new_username=data.username, new_password=data.password)
    if not updated:
        raise HTTPException(status_code=404, detail="User not found")
    return updated

@app.delete("/admin/users/{user_id}")
def admin_delete_user(user_id: int, admin=Depends(get_current_admin), db: Session = Depends(get_db)):
    success = delete_user(db, user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return {"result": "ok"}
