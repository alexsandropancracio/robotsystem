from datetime import datetime, timedelta
from typing import Optional, Any
import secrets

from jose import jwt, JWTError
from passlib.context import CryptContext
from fastapi.security import HTTPBearer

from backend.api.core.config import get_settings

settings = get_settings()

bearer_scheme = HTTPBearer()

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
)

# =========================
# PASSWORD
# =========================
def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(
    plain_password: str,
    hashed_password: str,
) -> bool:
    return pwd_context.verify(
        plain_password,
        hashed_password,
    )

# =========================
# JWT
# =========================
def create_access_token(
    subject: str | Any,
    expires_delta: Optional[timedelta] = None,
) -> str:
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )

    payload = {
        "sub": str(subject),
        "exp": expire,
    }

    return jwt.encode(
        payload,
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
    

# =========================
# TOKEN REGISTER
# =========================
def generate_email_token() -> str:
    return f"{secrets.randbelow(1000000):06d}"