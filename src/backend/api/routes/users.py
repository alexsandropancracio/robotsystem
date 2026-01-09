# backend/api/routes/users.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.api.deps.database import get_db
from backend.api.deps.auth import get_current_user
from backend.api.models.user import User
from backend.api.schemas.user import UserCreate, UserRead
from backend.api.services import user_service
from backend.api.core.exceptions import UserAlreadyExistsError

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)

# -------------------
# Registro de usuário
# -------------------
@router.post(
    "/register",
    response_model=UserRead,
    status_code=status.HTTP_201_CREATED,
)
def register_user(
    user_in: UserCreate,
    db: Session = Depends(get_db),
):
    try:
        return user_service.create_user_service(db, user_in)
    except UserAlreadyExistsError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e),
        )


# -------------------
# Listagem de usuários
# -------------------
@router.get("/", response_model=list[UserRead])
def list_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Lista todos os usuários (protegido)
    """
    return user_service.list_users_service(db)


# -------------------
# Buscar usuário por ID
# -------------------
@router.get("/{user_id}", response_model=UserRead)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Busca usuário pelo ID (protegido)
    """
    user = user_service.get_user_service(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado",
        )
    return user
