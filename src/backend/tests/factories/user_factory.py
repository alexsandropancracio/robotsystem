# tests/factories/user_factory.py
from sqlalchemy.orm import Session

from backend.api.models.user import User


def create_user(
    *,
    db: Session,
    email: str = "test@example.com",
    hashed_password: str = "fake-hash",
    is_active: bool = False,
    is_email_verified: bool = False,
) -> User:
    user = User(
        email=email,
        hashed_password=hashed_password,
        is_active=is_active,
        is_email_verified=is_email_verified,
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user
