from datetime import timedelta
from sqlalchemy.orm import Session

from backend.api.models.user import User
from backend.api.models.refresh_token import RefreshToken
from backend.api.core.security import (
    verify_password,
    create_token,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    REFRESH_TOKEN_EXPIRE_DAYS,
)

def authenticate_user(db: Session, email: str, password: str) -> User | None:
    user = db.query(User).filter(User.email == email).first()

    if not user:
        return None

    if not verify_password(password, user.hashed_password):
        return None

    if not user.is_active:
        return None

    return user

def generate_tokens(db: Session, user: User):
    access_token = create_token(
        subject=str(user.id),
        token_type="access",
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )

    refresh_token = create_token(
        subject=str(user.id),
        token_type="refresh",
        expires_delta=timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS),
    )

    db_refresh = RefreshToken(
        user_id=user.id,
        token=refresh_token,
    )

    db.add(db_refresh)
    db.commit()
    db.refresh(db_refresh)

    return access_token, refresh_token
