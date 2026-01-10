# backend/api/routes/me.py

from fastapi import APIRouter, Depends
from backend.api.core.auth import get_current_user
from backend.api.models.user import User
from backend.api.schemas.user import UserRead

router = APIRouter(
    prefix="/me",
    tags=["Me"],
)

@router.get("", response_model=UserRead)
def read_me(
    current_user: User = Depends(get_current_user),
):
    """
    Retorna o usuário autenticado
    """
    return UserRead.from_orm(current_user)
