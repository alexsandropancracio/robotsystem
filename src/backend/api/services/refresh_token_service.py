
from datetime import datetime, timedelta, timezone
import secrets
from typing import Optional

from sqlalchemy.orm import Session

from backend.api.models.refresh_token import RefreshToken
from backend.api.models.user import User
from backend.api.core.config import get_settings

settings = get_settings()


class RefreshTokenService:
    """
    Serviço responsável por criar, validar, revogar e rotacionar refresh tokens.
    """

    def __init__(self, db: Session):
        self.db = db

    # -------------------------------------------------
    # Criação
    # -------------------------------------------------
    def create_refresh_token(self, user: User) -> str:
        """
        Cria e persiste um refresh token para o usuário.
        Retorna APENAS a string do token.
        """
        expires_at = datetime.now(timezone.utc) + timedelta(
            minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES
        )

        token_str = secrets.token_urlsafe(64)

        refresh_token = RefreshToken(
            token=token_str,
            user_id=user.id,
            expires_at=expires_at,
            is_revoked=False,
        )

        self.db.add(refresh_token)
        self.db.commit()

        return token_str

    # -------------------------------------------------
    # Validação
    # -------------------------------------------------
    def validate_refresh_token(self, token_str: str) -> Optional[RefreshToken]:
        """
        Valida um refresh token:
        - existe
        - não revogado
        - não expirado
        """
        token = (
            self.db.query(RefreshToken)
            .filter_by(token=token_str, is_revoked=False)
            .first()
        )

        if not token:
            return None

        now = datetime.now(timezone.utc)

        if token.expires_at < now:
            token.is_revoked = True
            self.db.commit()
            return None

        return token

    # -------------------------------------------------
    # Revogação
    # -------------------------------------------------
    def revoke_refresh_token(self, token_str: str) -> bool:
        token = (
            self.db.query(RefreshToken)
            .filter_by(token=token_str, is_revoked=False)
            .first()
        )

        if not token:
            return False

        token.is_revoked = True
        self.db.commit()
        return True

    # -------------------------------------------------
    # Rotação
    # -------------------------------------------------
    def rotate_refresh_token(self, old_token_str: str) -> Optional[tuple[User, str]]:
        old_token = self.validate_refresh_token(old_token_str)
        if not old_token:
            return None

        user = old_token.user

        try:
            old_token.is_revoked = True
            new_token_str = self.create_refresh_token(user)
            self.db.commit()
            return user, new_token_str
        except Exception:
            self.db.rollback()
            return None

    # -------------------------------------------------
    # Limpeza (uso futuro - job / cron)
    # -------------------------------------------------
    def cleanup_expired_tokens(self) -> int:
        now = datetime.now(timezone.utc)

        expired_tokens = (
            self.db.query(RefreshToken)
            .filter(
                RefreshToken.expires_at < now,
                RefreshToken.is_revoked.is_(False),
            )
            .all()
        )

        for token in expired_tokens:
            token.is_revoked = True

        count = len(expired_tokens)

        if count:
            self.db.commit()

        return count
