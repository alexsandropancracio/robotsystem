# backend/api/schemas/auth.py
from pydantic import BaseModel, EmailStr, Field


# ------------------------
# LOGIN
# ------------------------
class LoginRequest(BaseModel):
    email: EmailStr
    password: str


# ------------------------
# TOKENS
# ------------------------
class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RefreshTokenRequest(BaseModel):
    refresh_token: str


# ------------------------
# ATIVAÇÃO DE CONTA
# ------------------------
class SendActivationRequest(BaseModel):
    email: EmailStr


class ActivateAccountRequest(BaseModel):
    email: EmailStr
    token: str = Field(
        ...,
        min_length=6,
        max_length=6,
        description="Código de ativação de 6 dígitos",
        examples=["123456"],
    )
