from sqlalchemy.orm import Session
from models.tag import Tag
from schemas.memo import MemoCreate, MemoUpdate
from sqlalchemy import func
from models.memo import Memo, memo_tags


def get_memos(
    db: Session,
    user_id: int,
    tag_ids: list[int] | None = None,
    category_id: int | None = None,
    important: int | None = None,
    keyword: str | None = None,
    sort: str = "created_desc"
):
    query = db.query(Memo).filter(Memo.user_id == user_id)

    # ---------------------
    # カテゴリ
    # ---------------------
    if category_id:
        query = query.filter(Memo.category_id == category_id)

    # ---------------------
    # 重要度
    # ---------------------
    if important:
        query = query.filter(Memo.important == important)

    # ---------------------
    # キーワード検索
    # ---------------------
    if keyword:
        like = f"%{keyword}%"
        query = query.filter(
            (Memo.title.ilike(like)) |
            (Memo.content.ilike(like))
        )

    # ---------------------
    # タグフィルタ（AND検索）
    # ---------------------
    if tag_ids:
        query = (
            query.join(memo_tags)
            .filter(memo_tags.c.tag_id.in_(tag_ids))
            .group_by(Memo.id)
            .having(func.count(Memo.id) == len(tag_ids))
        )

    # ---------------------
    # ソート
    # ---------------------
    if sort == "created_desc":
        query = query.order_by(Memo.created_at.desc())
    elif sort == "created_asc":
        query = query.order_by(Memo.created_at.asc())
    elif sort == "important_desc":
        query = query.order_by(Memo.important.desc())
    elif sort == "important_asc":
        query = query.order_by(Memo.important.asc())

    return query.all()

def get_memo(db: Session, memo_id: int, user_id: int):
    return db.query(Memo).filter(Memo.id == memo_id, Memo.user_id == user_id).first()

def create_memo(db: Session, memo: MemoCreate, user_id: int):
    db_memo = Memo(
        title=memo.title,
        content=memo.content,
        category_id=memo.category_id,
        file_paths=memo.file_paths,
        urls=memo.urls,
        important=memo.important,
        user_id=user_id
    )
    if memo.tag_ids:
        tags = db.query(Tag).filter(Tag.id.in_(memo.tag_ids), Tag.user_id == user_id).all()
        db_memo.tags = tags

    db.add(db_memo)
    db.commit()
    db.refresh(db_memo)
    return db_memo

def update_memo(db: Session, memo_id: int, memo: MemoUpdate, user_id: int):
    db_memo = get_memo(db, memo_id, user_id)
    if not db_memo:
        return None

    db_memo.title = memo.title
    db_memo.content = memo.content
    db_memo.category_id = memo.category_id
    db_memo.file_paths = memo.file_paths
    db_memo.urls = memo.urls
    db_memo.important = memo.important

    if memo.tag_ids is not None:
        tags = db.query(Tag).filter(Tag.id.in_(memo.tag_ids), Tag.user_id == user_id).all() if memo.tag_ids else []
        db_memo.tags = tags

    db.commit()
    db.refresh(db_memo)
    return db_memo

def delete_memo(db: Session, memo_id: int, user_id: int):
    db_memo = get_memo(db, memo_id, user_id)
    if not db_memo:
        return None
    db.delete(db_memo)
    db.commit()
    return True
