from datetime import datetime, timedelta, timezone
import secrets
import logging

from sqlalchemy.orm import Session

from backend.api.models.user import User
from backend.api.models.password_reset_token import PasswordResetToken
from backend.api.core.mail.mail_service import MailService
from backend.api.core.security.token import hash_token
from backend.api.core.auth import hash_password


logger = logging.getLogger("robotsystem.password_reset")

TOKEN_EXPIRATION_MINUTES = 30


class PasswordResetService:
    """
    Serviço responsável pelo fluxo completo de reset de senha.
    """

    def __init__(
        self,
        db: Session,
        mail_service: MailService,
    ) -> None:
        self.db = db
        self.mail_service = mail_service

    # -------------------------------------------------
    # REQUEST RESET
    # -------------------------------------------------
    def request_reset(self, email: str) -> None:
        """
        Solicita reset de senha.
        Resposta silenciosa para evitar enumeração de usuários.
        """

        user = (
            self.db.query(User)
            .filter(User.email == email)
            .first()
        )

        if not user:
            logger.info("Password reset solicitado para email inexistente")
            return

        # Invalida tokens anteriores
        (
            self.db.query(PasswordResetToken)
            .filter(
                PasswordResetToken.user_id == user.id,
                PasswordResetToken.used_at.is_(None),
            )
            .update(
                {"used_at": datetime.now(timezone.utc)},
                synchronize_session=False,
            )
        )

        raw_token = secrets.token_urlsafe(32)

        reset_token = PasswordResetToken(
            user_id=user.id,
            hashed_token=hash_token(raw_token),
            expires_at=datetime.now(timezone.utc)
            + timedelta(minutes=TOKEN_EXPIRATION_MINUTES),
        )

        self.db.add(reset_token)
        self.db.commit()

        logger.info(
            "Password reset token criado para user_id=%s",
            user.id,
        )

        self.mail_service.send_password_reset_email(
            email=user.email,
            token=raw_token,
            expires_in_minutes=TOKEN_EXPIRATION_MINUTES,
        )

    # -------------------------------------------------
    # CONFIRM RESET
    # -------------------------------------------------
    def reset_password(
        self,
        token: str,
        new_password: str,
        confirm_password: str,
    ) -> None:

        if new_password != confirm_password:
            raise ValueError("As senhas não coincidem")

        hashed = hash_token(token)

        reset_token = (
            self.db.query(PasswordResetToken)
            .filter(
                PasswordResetToken.hashed_token == hashed,
                PasswordResetToken.used_at.is_(None),
                PasswordResetToken.expires_at > datetime.now(timezone.utc),
            )
            .first()
        )

        if not reset_token:
            logger.warning("Token inválido ou expirado")
            raise ValueError("Token inválido ou expirado")

        user = reset_token.user

        user.hashed_password = hash_password(new_password)
        reset_token.used_at = datetime.now(timezone.utc)

        self.db.commit()

        logger.info(
            "Senha redefinida com sucesso para user_id=%s",
            user.id,
        )
