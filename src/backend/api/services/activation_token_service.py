import random
from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from backend.api.models.user import User
from backend.api.repositories.activation_token_repository import ActivationTokenRepository
from backend.api.core.exceptions import InvalidActivationTokenError


TOKEN_EXPIRATION_MINUTES = 15


class ActivationTokenService:

    def __init__(self, db: Session):
        self.db = db
        self.repo = ActivationTokenRepository(db)

    def generate_token(self) -> str:
        return f"{random.randint(0, 999999):06d}"

    def create_activation_token(self, user: User) -> str:
        self.repo.invalidate_all_for_user(
            user_id=user.id,
        )

        token = self.generate_token()
        expires_at = datetime.utcnow() + timedelta(
            minutes=TOKEN_EXPIRATION_MINUTES
        )

        self.repo.create(
            user_id=user.id,
            token=token,
            expires_at=expires_at,
        )

        self.db.commit()

        return token

    def activate_user(
        self,
        *,
        user: User,
        token: str,
    ) -> None:
        activation_token = self.repo.get_valid_token(
            user_id=user.id,
            token=token,
        )

        if not activation_token:
            raise InvalidActivationTokenError()

        if activation_token.expires_at < datetime.utcnow():
            raise InvalidActivationTokenError("Token expirado")

        activation_token.is_used = True
        user.is_active = True
        user.is_email_verified = True

        self.db.commit()
