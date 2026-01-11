# backend/api/services/user_service.py
from datetime import datetime
from typing import Optional

from sqlalchemy.orm import Session

from backend.api.models.user import User
from backend.api.schemas.user import UserCreate, UserRead
from backend.api.repositories.user_repository import UserRepository
from backend.api.core.auth import hash_password
from backend.api.core.exceptions import UserAlreadyExistsError

repo = UserRepository()

# -------------------
# Criação de usuário
# -------------------
def create_user_service(db: Session, user_in: UserCreate) -> UserRead:
    if repo.get_by_email(db, user_in.email):
        raise UserAlreadyExistsError("Usuário já existe")

    user = User(
        email=user_in.email,
        full_name=getattr(user_in, "full_name", None),
        hashed_password=hash_password(user_in.password),
        is_active=False,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return UserRead.from_orm(user)


# -------------------
# Listar usuários
# -------------------
def list_users_service(db: Session) -> list[UserRead]:
    return [UserRead.from_orm(u) for u in repo.get_all(db)]


# -------------------
# Buscar usuário por ID
# -------------------
def get_user_service(db: Session, user_id: int) -> Optional[UserRead]:
    user = repo.get(db, user_id)
    return UserRead.from_orm(user) if user else None
