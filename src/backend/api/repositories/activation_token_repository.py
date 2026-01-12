#backend/api/repositories/activation_token_repository.py
from datetime import datetime
from sqlalchemy.orm import Session

from backend.api.models.activation_token import ActivationToken

class ActivationTokenRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, *, user_id: int, token: str, expires_at: datetime) -> ActivationToken:
        activation_token = ActivationToken(
            user_id=user_id,
            token=token,
            expires_at=expires_at,
            is_used=False,
        )
        self.db.add(activation_token)
        self.db.commit()
        self.db.refresh(activation_token)
        return activation_token

    def get_valid_token(self, *, user_id: int, token: str) -> ActivationToken | None:
        return (
            self.db.query(ActivationToken)
            .filter(
                ActivationToken.user_id == user_id,
                ActivationToken.token == token,
                ActivationToken.is_used.is_(False),
                ActivationToken.expires_at > datetime.utcnow(),
            )
            .first()
        )

    def invalidate_all_for_user(self, *, user_id: int) -> None:
        (
            self.db.query(ActivationToken)
            .filter(
                ActivationToken.user_id == user_id,
                ActivationToken.is_used.is_(False),
            )
            .update({"is_used": True})
        )
        self.db.commit()