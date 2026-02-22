from sqlalchemy.orm import Session
from models.memo import Memo
from models.tag import Tag
from schemas.memo import MemoCreate, MemoUpdate

def get_memos(db: Session, user_id: int):
    return db.query(Memo).filter(Memo.user_id == user_id).all()

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
