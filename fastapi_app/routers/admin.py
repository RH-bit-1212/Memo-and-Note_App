# fastapi_app/routers/admin.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from db import get_db

from auth import get_current_admin

from crud.user import (
    create_user,
    get_users,
    get_user,
    update_user,
    delete_user,
)

from schemas.user import (
    UserCreate,
    UserResponse,
)

router = APIRouter(
    prefix="/admin/users",
    tags=["Admin"]
)

# ===================================================
# ユーザー CRUD（管理者用）
# ===================================================
@router.get("", response_model=list[UserResponse])
def admin_read_users(
    admin=Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    return get_users(db)


@router.get("/{user_id}", response_model=UserResponse)
def admin_read_user(
    user_id: int,
    admin=Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    user = get_user(db, user_id)

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return user


@router.post("", response_model=UserResponse)
def admin_create_user(
    user: UserCreate,
    admin=Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    return create_user(db, user)


@router.put("/{user_id}", response_model=UserResponse)
def admin_update_user(
    user_id: int,
    data: UserCreate,
    admin=Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    updated = update_user(
        db,
        user_id,
        new_username=data.username,
        new_password=data.password
    )

    if not updated:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return updated


@router.delete("/{user_id}")
def admin_delete_user(
    user_id: int,
    admin=Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    success = delete_user(db, user_id)

    if not success:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return {"result": "ok"}