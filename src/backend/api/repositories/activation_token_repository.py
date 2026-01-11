from datetime import datetime
from sqlalchemy.orm import Session

from backend.api.models.activation_token import ActivationToken

class ActivationTokenRepository:

    def create(
        self,
        db: Session,
        *,
        user_id: int,
        token: str,
        expires_at: datetime,
    ) -> ActivationToken:
        activation_token = ActivationToken(
            user_id=user_id,
            token=token,
            expires_at=expires_at,
            is_used=False,
        )
        db.add(activation_token)
        return activation_token

    def get_valid_token(
        self,
        db: Session,
        *,
        user_id: int,
        token: str,
    ) -> ActivationToken | None:
        return (
            db.query(ActivationToken)
            .filter(
                ActivationToken.user_id == user_id,
                ActivationToken.token == token,
                ActivationToken.is_used.is_(False),
                ActivationToken.expires_at > datetime.utcnow(),
            )
            .first()
        )

    def invalidate_all_for_user(
        self,
        db: Session,
        *,
        user_id: int,
    ) -> None:
        (
            db.query(ActivationToken)
            .filter(
                ActivationToken.user_id == user_id,
                ActivationToken.is_used.is_(False),
            )
            .update({"is_used": True})
        )
