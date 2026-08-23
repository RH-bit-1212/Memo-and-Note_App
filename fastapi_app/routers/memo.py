from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from typing import List, Optional

from db import get_db

from auth import get_current_user

from crud.memo import (
    get_memos,
    get_memo,
    create_memo,
    update_memo,
    delete_memo,
)

from schemas.memo import (
    MemoCreate,
    MemoUpdate,
    MemoResponse,
)

router = APIRouter(
    prefix="/memos",
    tags=["Memo"]
)

# ===================================================
# メモ CRUD（ユーザー制約）
# ===================================================
@router.get("", response_model=list[MemoResponse])
def read_memos(
    tag_ids: List[int] = Query(default=[]),
    category_id: Optional[int] = None,
    important: Optional[int] = None,
    keyword: Optional[str] = None,
    sort: str = "created_desc",
    user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return get_memos(
        db=db,
        user_id=user.id,
        tag_ids=tag_ids,
        category_id=category_id,
        important=important,
        keyword=keyword,
        sort=sort
    )


@router.get("/{memo_id}", response_model=MemoResponse)
def read_memo(
    memo_id: int,
    user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    memo = get_memo(db, memo_id, user.id)

    if not memo:
        raise HTTPException(
            status_code=404,
            detail="Memo not found"
        )

    return memo


@router.post("", response_model=MemoResponse)
def create_memo_endpoint(
    memo: MemoCreate,
    user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return create_memo(db, memo, user.id)


@router.put("/{memo_id}", response_model=MemoResponse)
def update_memo_endpoint(
    memo_id: int,
    memo: MemoUpdate,
    user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    updated = update_memo(
        db,
        memo_id,
        memo,
        user.id
    )

    if not updated:
        raise HTTPException(
            status_code=404,
            detail="Memo not found"
        )

    return updated


@router.delete("/{memo_id}")
def delete_memo_endpoint(
    memo_id: int,
    user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    ok = delete_memo(
        db,
        memo_id,
        user.id
    )

    if not ok:
        raise HTTPException(
            status_code=404,
            detail="Memo not found"
        )

    return {"result": "ok"}