# backend/api/services/user_service.py
from datetime import datetime, timedelta
from typing import Optional

from sqlalchemy.orm import Session

from backend.api.models.user import User
from backend.api.schemas.user import (
    UserCreate,
    UserLogin,
    Token,
    UserRead,
)
from backend.api.repositories.user_repository import UserRepository
from backend.api.core.auth import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
    decode_refresh_token,
)
from backend.api.core.config import get_settings
from backend.api.core.exceptions import InvalidCredentialsError


settings = get_settings()
repo = UserRepository()

# -------------------
# Criação de usuário
# -------------------
def create_user_service(db: Session, user_in: UserCreate) -> UserRead:
    """
    Cria um novo usuário com hash de senha
    """
    if repo.get_by_email(db, user_in.email):
        raise ValueError("Usuário já existe")

    user = User(
        email=user_in.email,
        full_name=getattr(user_in, "full_name", None),
        hashed_password=hash_password(user_in.password),
        is_active=True,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return UserRead.from_orm(user)


# -------------------
# Login de usuário
# -------------------
def login_user_service(db: Session, user_in: UserLogin) -> Token:
    """
    Autentica usuário e retorna access + refresh tokens
    """
    user = repo.get_by_email(db, user_in.email)

    if not user or not verify_password(user_in.password, user.password):
        raise InvalidCredentialsError("Credenciais inválidas")

    access_token = create_access_token(
        {"sub": str(user.id)},
        expires_delta=timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        ),
    )

    refresh_token = create_refresh_token(
        {"sub": str(user.id)},
        expires_delta=timedelta(
            days=settings.REFRESH_TOKEN_EXPIRE_DAYS
        ),
    )


    return Token(
            access_token=access_token,
            refresh_token=refresh_token,
        )


# -------------------
# Refresh token
# -------------------
def refresh_token_service(db: Session, token: str) -> Optional[Token]:
    """
    Recebe um refresh token válido e retorna novos tokens
    """
    payload = decode_refresh_token(token)
    if not payload or "sub" not in payload:
        return None

    user = repo.get(db, int(payload["sub"]))
    if not user:
        return None

    access_token = create_access_token(
        {"sub": str(user.id)},
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
    )

    refresh_token = create_refresh_token(
        {"sub": str(user.id)},
        expires_delta=timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
    )

    return Token(
        access_token=access_token,
        refresh_token=refresh_token,
    )


# -------------------
# Listar usuários
# -------------------
def list_users_service(db: Session) -> list[UserRead]:
    return [UserRead.from_orm(u) for u in repo.get_all(db)]


# -------------------
# Buscar usuário por ID
# -------------------
def get_user_service(db: Session, user_id: int) -> Optional[UserRead]:
    user = repo.get(db, user_id)
    return UserRead.from_orm(user) if user else None
