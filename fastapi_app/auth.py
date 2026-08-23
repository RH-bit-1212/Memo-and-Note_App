# fastapi_app/auth.py

from fastapi import Depends, Header, HTTPException
from sqlalchemy.orm import Session
from jose import jwt, JWTError
import os

from db import get_db
from crud.user import get_user_by_username

# ===================================================
# JWT 設定
# ===================================================
SECRET_KEY = os.getenv("SECRET_KEY")

if not SECRET_KEY:
    raise RuntimeError("SECRET_KEY is not configured")

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 3

# ===================================================
# JWT デコード
# ===================================================
def decode_token(token: str):
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        username = payload.get("sub")

        if not username:
            raise HTTPException(
                status_code=401,
                detail="Invalid token payload"
            )

        return username

    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )


# ===================================================
# 認証 Dependencies
# ===================================================
def get_current_user(
    authorization: str = Header(None),
    db: Session = Depends(get_db)
):
    if not authorization:
        raise HTTPException(
            status_code=401,
            detail="Authorization header missing"
        )

    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=401,
            detail=f"Invalid authorization header: {authorization}"
        )

    token = authorization.split(" ")[1]

    username = decode_token(token)

    user = get_user_by_username(db, username)

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return user


def get_current_admin(
    user=Depends(get_current_user)
):
    if user.role != "admin":
        raise HTTPException(
            status_code=403,
            detail="Admin only"
        )

    return user