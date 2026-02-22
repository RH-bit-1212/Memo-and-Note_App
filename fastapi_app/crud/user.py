from sqlalchemy.orm import Session
from models.user import User
from schemas.user import UserCreate, UserLogin
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# --- パスワードハッシュ化（最大72バイトに切り詰め） ---
def get_password_hash(password: str) -> str:
    password_bytes = password.encode("utf-8")[:72]
    return pwd_context.hash(password_bytes)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    plain_bytes = plain_password.encode("utf-8")[:72]
    return pwd_context.verify(plain_bytes, hashed_password)

# --- ユーザー作成 ---
def create_user(db: Session, user: UserCreate):
    db_user = User(
        username=user.username,
        hashed_password=get_password_hash(user.password),
        role=getattr(user, "role", "user")  # role がなければ "user"
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# --- 全ユーザー取得 ---
def get_users(db: Session):
    return db.query(User).all()

# --- ID指定でユーザー取得 ---
def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

# --- ユーザー名で取得 ---
def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

# --- 認証 ---
def authenticate_user(db: Session, username: str, password: str):
    user = get_user_by_username(db, username)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user

# --- ユーザー更新 ---
def update_user(db: Session, user_id: int, new_username: str = None, new_password: str = None, new_role: str = None):
    user = get_user(db, user_id)
    if not user:
        return None
    if new_username:
        user.username = new_username
    if new_password:
        user.hashed_password = get_password_hash(new_password)
    if new_role:
        user.role = new_role
    db.commit()
    db.refresh(user)
    return user

# --- ユーザー削除 ---
def delete_user(db: Session, user_id: int):
    user = get_user(db, user_id)
    if not user:
        return False
    db.delete(user)
    db.commit()
    return True
