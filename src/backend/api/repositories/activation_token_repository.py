from datetime import datetime
from typing import Optional
from sqlalchemy.orm import Session
from backend.api.models.activation_token import ActivationToken

class ActivationTokenRepository:

    def __init__(self, db: Session):
        self.db = db

    # -------------------------------------------------
    # CREATE
    # -------------------------------------------------
    def create(
        self,
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
        self.db.add(activation_token)
        return activation_token

    # -------------------------------------------------
    # READ
    # -------------------------------------------------
    def get_active_token_for_user(
        self,
        *,
        user_id: int,
    ) -> Optional[ActivationToken]:
        """
        Retorna o token ativo mais recente do usuário,
        considerando não usado e não expirado (UTC).
        """
        return (
            self.db.query(ActivationToken)
            .filter(
                ActivationToken.user_id == user_id,
                ActivationToken.is_used.is_(False),
                ActivationToken.expires_at > datetime.utcnow(),
            )
            .order_by(ActivationToken.expires_at.desc())
            .first()
        )

    # -------------------------------------------------
    # UPDATE
    # -------------------------------------------------
    def invalidate_all_for_user(
        self,
        *,
        user_id: int,
    ) -> None:
        """
        Marca todos os tokens não usados do usuário como usados.
        """
        (
            self.db.query(ActivationToken)
            .filter(
                ActivationToken.user_id == user_id,
                ActivationToken.is_used.is_(False),
            )
            .update(
                {"is_used": True},
                synchronize_session=False,
            )
        )
