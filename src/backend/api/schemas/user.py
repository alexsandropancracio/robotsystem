# backend/api/schemas/user.py
from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime
from pydantic import validator
import re

# -------------------
# Schemas base
# -------------------
class UserBase(BaseModel):
    email: EmailStr
    full_name: str | None = None  # Opcional, caso queira armazenar nome completo

# -------------------
# Criação de usuário (input)
# -------------------
class UserCreate(UserBase):
    password: str

    @validator("password")
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

    model_config = ConfigDict(from_attributes=True)  # SQLAlchemy -> Pydantic

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
