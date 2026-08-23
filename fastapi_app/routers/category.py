from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from db import get_db

from auth import get_current_user

from crud.category import (
    get_categories,
    get_category,
    create_category,
    update_category,
    delete_category,
)

from schemas.category import (
    CategoryCreate,
    CategoryUpdate,
    CategoryResponse,
)

router = APIRouter(
    prefix="/categories",
    tags=["Category"]
)

# ===================================================
# カテゴリ CRUD（ユーザー制約）
# ===================================================

@router.get("", response_model=list[CategoryResponse])
def read_categories(
    user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return get_categories(db, user.id)


@router.get("/{category_id}", response_model=CategoryResponse)
def read_category(
    category_id: int,
    user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    category = get_category(db, category_id, user.id)

    if not category:
        raise HTTPException(
            status_code=404,
            detail="Category not found"
        )

    return category


@router.post("", response_model=CategoryResponse)
def create_category_endpoint(
    category: CategoryCreate,
    user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return create_category(db, category, user.id)


@router.put("/{category_id}", response_model=CategoryResponse)
def update_category_endpoint(
    category_id: int,
    category: CategoryUpdate,
    user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    updated = update_category(
        db,
        category_id,
        category,
        user.id
    )

    if not updated:
        raise HTTPException(
            status_code=404,
            detail="Category not found"
        )

    return updated


@router.delete("/{category_id}")
def delete_category_endpoint(
    category_id: int,
    user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    ok = delete_category(
        db,
        category_id,
        user.id
    )

    if not ok:
        raise HTTPException(
            status_code=404,
            detail="Category not found"
        )

    return {"result": "ok"}