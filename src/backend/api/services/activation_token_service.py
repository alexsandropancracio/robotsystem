# backend/api/services/activation_token_service.py
import random
from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from backend.api.models.user import User
from backend.api.repositories.activation_token_repository import (
    ActivationTokenRepository
)
from backend.api.core.exceptions import InvalidActivationTokenError
from backend.api.core.security.token import (
    hash_token,
    verify_token,
)

TOKEN_EXPIRATION_MINUTES = 15


class ActivationTokenService:

    def __init__(self, db: Session):
        self.db = db
        self.repo = ActivationTokenRepository(db)

    # -------------------------------------------------
    # TOKEN
    # -------------------------------------------------
    def generate_token(self) -> str:
        """
        Gera um token numérico de 6 dígitos.
        """
        return f"{random.randint(0, 999999):06d}"

    # -------------------------------------------------
    # CREATE
    # -------------------------------------------------
    def create_activation_token(self, user: User) -> str:
        """
        Cria um novo token de ativação para o usuário.
        Invalida qualquer token anterior ainda ativo.
        """

        if user.is_active:
            raise InvalidActivationTokenError(
                "Conta já está ativada"
            )

        # Invalida tokens anteriores
        self.repo.invalidate_all_for_user(user_id=user.id)

        token = self.generate_token()
        token_hash = hash_token(token)
        expires_at = datetime.utcnow() + timedelta(
            minutes=TOKEN_EXPIRATION_MINUTES
        )

        self.repo.create(
            user_id=user.id,
            token=token_hash,
            expires_at=expires_at,
        )

        self.db.commit()
        return token

    # -------------------------------------------------
    # ACTIVATE
    # -------------------------------------------------
    def activate_user(self, *, user: User, token: str) -> None:
        """
        Ativa o usuário se o token for válido.
        """

        if user.is_active:
            raise InvalidActivationTokenError(
                "Conta já está ativada"
            )

        activation_token = self.repo.get_active_token_for_user(
            user_id=user.id
        )

        if not activation_token:
            raise InvalidActivationTokenError(
                "Token inválido ou expirado"
            )

        # Validação do token (regra de domínio)
        if not verify_token(token, activation_token.token):
            raise InvalidActivationTokenError(
                "Token inválido ou expirado"
            )


        activation_token.is_used = True
        user.is_active = True
        user.is_email_verified = True

        self.db.commit()

    # -------------------------------------------------
    # ACTIVATE BY EMAIL
    # -------------------------------------------------
    def activate_account(self, *, email: str, token: str) -> None:
        """
        Ativa a conta a partir do e-mail e token.
        """

        user = (
            self.db.query(User)
            .filter(User.email == email)
            .first()
        )

        if not user:
            raise InvalidActivationTokenError(
                "Token inválido ou expirado"
            )

        self.activate_user(
            user=user,
            token=token,
        )
