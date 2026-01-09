# backend/api/schemas/user.py
from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime

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
