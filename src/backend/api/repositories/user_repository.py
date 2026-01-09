# backend/api/repositories/user_repository.py
from sqlalchemy.orm import Session
from typing import Optional, List

from backend.api.models.user import User
from backend.api.schemas.user import UserCreate

class UserRepository:
    """
    Repositório para operações CRUD de User
    """

    # -------------------
    # Criar usuário
    # -------------------
    def create(self, db: Session, user_in: UserCreate) -> User:
        user = User(
            email=user_in.email,
            full_name=getattr(user_in, "full_name", None),
            password=getattr(user_in, "password", None),  # já deve vir hash do service
            is_active=True
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    # -------------------
    # Buscar usuário pelo ID
    # -------------------
    def get(self, db: Session, user_id: int) -> Optional[User]:
        return db.query(User).filter(User.id == user_id).first()

    # -------------------
    # Buscar usuário pelo email
    # -------------------
    def get_by_email(self, db: Session, email: str) -> Optional[User]:
        return db.query(User).filter(User.email == email).first()

    # -------------------
    # Listar todos os usuários
    # -------------------
    def get_all(self, db: Session) -> List[User]:
        return db.query(User).all()

    # -------------------
    # Atualizar usuário (opcional)
    # -------------------
    def update(self, db: Session, user: User, **kwargs) -> User:
        for attr, value in kwargs.items():
            setattr(user, attr, value)
        db.commit()
        db.refresh(user)
        return user

    # -------------------
    # Deletar usuário (opcional)
    # -------------------
    def delete(self, db: Session, user: User) -> None:
        db.delete(user)
        db.commit()
