from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime, timezone

from backend.api.core.auth import get_current_user
from backend.api.deps.database import get_db
from backend.api.models.user import User
from backend.api.models.license import License


def get_current_user_with_license(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> User:
    """
    Retorna o usuário apenas se ele possuir uma licença ativa e válida.
    """

    license_obj = (
        db.query(License)
        .filter(
            License.user_id == current_user.id,
            License.is_active.is_(True),
        )
        .first()
    )

    if not license_obj:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuário não possui licença ativa",
        )

    # valida expiração (se existir)
    if license_obj.expires_at:
        now = datetime.now(timezone.utc)
        if license_obj.expires_at < now:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Licença expirada",
            )

    return current_user

