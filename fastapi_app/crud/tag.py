from sqlalchemy.orm import Session
from models.tag import Tag
from schemas.tag import TagCreate, TagUpdate

def get_tags(db: Session, user_id: int):
    return db.query(Tag).filter(Tag.user_id == user_id).all()

def get_tag(db: Session, tag_id: int, user_id: int):
    return db.query(Tag).filter(Tag.id == tag_id, Tag.user_id == user_id).first()

def create_tag(db: Session, tag: TagCreate, user_id: int):
    db_tag = Tag(name=tag.name, color=tag.color, user_id=user_id)
    db.add(db_tag)
    db.commit()
    db.refresh(db_tag)
    return db_tag

def update_tag(db: Session, tag_id: int, tag: TagUpdate, user_id: int):
    db_tag = get_tag(db, tag_id, user_id)
    if not db_tag:
        return None
    db_tag.name = tag.name
    db_tag.color = tag.color
    db.commit()
    db.refresh(db_tag)
    return db_tag

def delete_tag(db: Session, tag_id: int, user_id: int):
    db_tag = get_tag(db, tag_id, user_id)
    if not db_tag:
        return None
    db.delete(db_tag)
    db.commit()
    return True
