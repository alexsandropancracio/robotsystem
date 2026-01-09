from fastapi import Depends, HTTPException, status
from backend.api.deps.auth import get_current_user
from backend.api.models.user import User

def require_admin(
    current_user: User = Depends(get_current_user),
):
    if not getattr(current_user, "is_admin", False):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso restrito a administradores",
        )
    return current_user
