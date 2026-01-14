# backend/api/repositories/user_repository.py
from typing import Optional, List

from sqlalchemy.orm import Session

from backend.api.models.user import User


class UserRepository:
    """
    Repositório para operações de persistência de User
    (Somente acesso ao banco — SEM regra de negócio)
    """

    # -------------------
    # Criar usuário
    # -------------------
    def create(self, db: Session, user: User) -> User:
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
    # Atualizar usuário
    # -------------------
    def update(self, db: Session, user: User, **kwargs) -> User:
        for attr, value in kwargs.items():
            if hasattr(user, attr):
                setattr(user, attr, value)

        db.commit()
        db.refresh(user)
        return user

    # -------------------
    # Deletar usuário
    # -------------------
    def delete(self, db: Session, user: User) -> None:
        db.delete(user)
        db.commit()
