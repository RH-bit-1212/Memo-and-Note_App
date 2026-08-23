from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from db import get_db

from auth import get_current_user

from crud.tag import (
    get_tags,
    get_tag,
    create_tag,
    update_tag,
    delete_tag,
)

from schemas.tag import (
    TagCreate,
    TagUpdate,
    TagResponse,
)

router = APIRouter(
    prefix="/tags",
    tags=["Tag"]
)

# ===================================================
# タグ CRUD（ユーザー制約）
# ===================================================

@router.get("", response_model=list[TagResponse])
def read_tags(
    user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return get_tags(db, user.id)


@router.get("/{tag_id}", response_model=TagResponse)
def read_tag(
    tag_id: int,
    user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    tag = get_tag(db, tag_id, user.id)

    if not tag:
        raise HTTPException(
            status_code=404,
            detail="Tag not found"
        )

    return tag


@router.post("", response_model=TagResponse)
def create_tag_endpoint(
    tag: TagCreate,
    user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return create_tag(db, tag, user.id)


@router.put("/{tag_id}", response_model=TagResponse)
def update_tag_endpoint(
    tag_id: int,
    tag: TagUpdate,
    user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    updated = update_tag(
        db,
        tag_id,
        tag,
        user.id
    )

    if not updated:
        raise HTTPException(
            status_code=404,
            detail="Tag not found"
        )

    return updated


@router.delete("/{tag_id}")
def delete_tag_endpoint(
    tag_id: int,
    user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    ok = delete_tag(
        db,
        tag_id,
        user.id
    )

    if not ok:
        raise HTTPException(
            status_code=404,
            detail="Tag not found"
        )

    return {"result": "ok"}