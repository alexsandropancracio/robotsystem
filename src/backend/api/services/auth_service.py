from datetime import timedelta
from sqlalchemy.orm import Session

from backend.api.models.user import User
from backend.api.repositories.user_repository import UserRepository
from backend.api.core.auth import (
    verify_password,
    create_access_token,
)
from backend.api.core.config import get_settings
from backend.api.services.refresh_token_service import RefreshTokenService
from backend.api.core.exceptions import InvalidCredentialsError

settings = get_settings()


# -------------------------------------------------
# Autenticação básica
# -------------------------------------------------
def authenticate_user(
    db: Session,
    email: str,
    password: str,
) -> User:
    repo = UserRepository()
    user = repo.get_by_email(db, email)

    if not user or not verify_password(password, user.hashed_password):
        raise InvalidCredentialsError("Email ou senha inválidos")

    if not user.is_active:
        raise InvalidCredentialsError("Usuário inativo")

    return user


# -------------------------------------------------
# Login (orquestrador)
# -------------------------------------------------
def login_service(
    db: Session,
    email: str,
    password: str,
):
    """
    Orquestra o login do usuário:
    - valida credenciais
    - gera access token
    - cria refresh token
    """
    user = authenticate_user(db, email, password)

    access_token = create_access_token(
    {"sub": str(user.id)},
    expires_delta=timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    ),
)

    refresh_service = RefreshTokenService(db)
    refresh_token = refresh_service.create_refresh_token(user)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }
