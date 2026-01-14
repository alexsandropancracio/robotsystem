# backend/api/core/auth.py
import logging
import hashlib
from datetime import datetime, timedelta
from typing import Optional

from jose import jwt, JWTError
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from sqlalchemy.orm import Session
from passlib.context import CryptContext

from backend.api.models.user import User
from backend.api.deps.database import get_db
from backend.api.repositories.user_repository import UserRepository
from backend.api.core.config import get_settings

# -------------------------------------------------
# Logging
# -------------------------------------------------
logger = logging.getLogger("robotsystem.auth")
if not logger.handlers:
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter("[%(levelname)s] %(message)s"))
    logger.addHandler(handler)
logger.setLevel(logging.INFO)

# -------------------------------------------------
# Configurações
# -------------------------------------------------
settings = get_settings()
PEPPER = getattr(settings, "PEPPER", "")

bearer_scheme = HTTPBearer()
repo = UserRepository()

# -------------------------------------------------
# Passlib
# -------------------------------------------------
pwd_context = CryptContext(
    schemes=["argon2"],
    deprecated="auto",
)

# -------------------------------------------------
# Helpers
# -------------------------------------------------
def _pre_hash_password(password: str) -> str:
    """
    Aplica SHA-256 em (senha + pepper) para evitar limites
    """
    combined = f"{password}{PEPPER}".encode("utf-8")
    return hashlib.sha256(combined).hexdigest()

# -------------------
# Hash de senha
# -------------------
def hash_password(password: str) -> str:
    """
    Gera hash seguro da senha (SHA-256 + Argon2)
    """
    pre_hash = _pre_hash_password(password)
    return pwd_context.hash(pre_hash)

def verify_password(password: str, hashed: str) -> bool:
    """
    Verifica senha usando SHA-256 + Argon2
    """
    pre_hash = _pre_hash_password(password)
    return pwd_context.verify(pre_hash, hashed)

# -------------------
# Access Token (JWT)
# -------------------
def create_access_token(
    data: dict,
    expires_delta: Optional[timedelta] = None,
) -> str:
    to_encode = data.copy()

    expire = datetime.utcnow() + (
        expires_delta
        if expires_delta
        else timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    to_encode.update({"exp": expire})

    return jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )

def decode_access_token(token: str) -> Optional[dict]:
    try:
        return jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )
    except JWTError:
        return None

# -------------------
# Dependency FastAPI
# -------------------
def get_current_user(
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> User:
    token = credentials.credentials
    payload = decode_access_token(token)

    if not payload or "sub" not in payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido",
        )

    user_id = int(payload["sub"])
    user = repo.get(db, user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário não encontrado",
        )

    return user
