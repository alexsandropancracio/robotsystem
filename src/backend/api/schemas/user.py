# backend/api/schemas/user.py
from datetime import datetime
import re

from pydantic import BaseModel, EmailStr, ConfigDict, field_validator

# -------------------
# Schemas base
# -------------------
class UserBase(BaseModel):
    email: EmailStr
    full_name: str | None = None


# -------------------
# Criação de usuário (input)
# -------------------
class UserCreate(UserBase):
    password: str

    @field_validator("password")
    @classmethod
    def password_strong(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("Senha deve ter pelo menos 8 caracteres")
        if not re.search(r"[A-Z]", v):
            raise ValueError("Senha deve conter pelo menos uma letra maiúscula")
        if not re.search(r"\d", v):
            raise ValueError("Senha deve conter pelo menos um número")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", v):
            raise ValueError("Senha deve conter pelo menos um símbolo")
        return v


# -------------------
# Usuário para leitura (output)
# -------------------
class UserRead(UserBase):
    id: int
    is_active: bool = True
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


# -------------------
# Login de usuário (input)
# -------------------
class UserLogin(BaseModel):
    email: EmailStr
    password: str


# -------------------
# Token (output de login / refresh)
# -------------------
class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
