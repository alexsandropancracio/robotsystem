# backend/api/core/security/token.py

import secrets
import hashlib
import hmac


def generate_token(length: int = 6) -> str:
    """
    Gera um token numérico seguro.
    Ex: 482931
    """
    return ''.join(str(secrets.randbelow(10)) for _ in range(length))


def hash_token(token: str) -> str:
    """
    Retorna o hash SHA-256 do token.
    """
    return hashlib.sha256(token.encode()).hexdigest()


def verify_token(token: str, hashed_token: str) -> bool:
    """
    Compara token informado com hash salvo no banco.
    """
    return hmac.compare_digest(
        hash_token(token),
        hashed_token
    )
