# backend/api/services/refresh_token_service.py

from datetime import datetime, timedelta, timezone
import secrets
from typing import Optional

from sqlalchemy.orm import Session

from backend.api.models.refresh_token import RefreshToken
from backend.api.models.user import User
from backend.api.core.config import get_settings
#from backend.api.services.logging import log_refresh


settings = get_settings()


class RefreshTokenService:
    """
    Serviço responsável por criar, validar, revogar e rotacionar refresh tokens.
    """

    def __init__(self, db: Session):
        self.db = db

    def create_refresh_token(
        self,
        user: User,
        expires_in: Optional[int] = None,
    ) -> RefreshToken:
        """
        Cria um refresh token válido para um usuário.
        """
        expires_in = expires_in or settings.REFRESH_TOKEN_EXPIRE_MINUTES
        expires_at = datetime.now(timezone.utc) + timedelta(minutes=expires_in)

        token = secrets.token_urlsafe(64)

        refresh_token = RefreshToken(
            token=token,
            user_id=user.id,
            expires_at=expires_at,
            is_revoked=False,
        )

        self.db.add(refresh_token)
        self.db.commit()
        self.db.refresh(refresh_token)

        return refresh_token

    def revoke_refresh_token(self, token_str: str) -> bool:
        """
        Revoga um refresh token ativo.
        """
        token = (
            self.db.query(RefreshToken)
            .filter(
                RefreshToken.token == token_str,
                RefreshToken.is_revoked.is_(False),
            )
            .first()
        )

        if not token:
            return False

        token.is_revoked = True
        self.db.commit()
        return True

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
            # 🔒 token expirado é automaticamente revogado
            token.is_revoked = True
            self.db.commit()
            return None

        return token

    def rotate_refresh_token(self, old_token_str: str) -> Optional[RefreshToken]:
        """
        Rotaciona refresh token:
        - valida o token antigo
        - revoga o token antigo
        - cria um novo token
        """
        old_token = self.validate_refresh_token(old_token_str)

        if not old_token:
            return None

        user = old_token.user

        # 🔐 LOG de uso do refresh token
        #log_refresh(user.email)

        # 🔄 rotação atômica
        old_token.is_revoked = True
        new_token = self.create_refresh_token(user)

        return new_token

    def cleanup_expired_tokens(self) -> int:
        """
        Revoga tokens expirados que ainda não foram revogados.
        Retorna a quantidade de tokens limpos.
        """
        now = datetime.now(timezone.utc)

        expired_tokens = (
            self.db.query(RefreshToken)
            .filter(
                RefreshToken.expires_at < now,
                RefreshToken.is_revoked.is_(False),
            )
            .all()
        )

        count = 0
        for token in expired_tokens:
            token.is_revoked = True
            count += 1

        if count > 0:
            self.db.commit()

        return count
