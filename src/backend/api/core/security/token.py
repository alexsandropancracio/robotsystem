# backend/api/core/security/token.py
import hashlib
import hmac

from backend.api.core.config import get_settings

settings = get_settings()


def hash_token(token: str) -> str:
    """
    Gera hash seguro do token usando HMAC + SHA256.
    """
    return hmac.new(
        key=settings.SECRET_KEY.encode(),
        msg=token.encode(),
        digestmod=hashlib.sha256,
    ).hexdigest()


def verify_token(token: str, hashed_token: str) -> bool:
    """
    Compara token em texto puro com hash armazenado.
    """
    return hmac.compare_digest(
        hash_token(token),
        hashed_token,
    )
