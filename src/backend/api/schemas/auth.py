# backend/api/schemas/auth.py
from pydantic import BaseModel, EmailStr, Field

class LoginRequest(BaseModel):
    email: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class RefreshTokenRequest(BaseModel):
    refresh_token: str

class ActivateAccountRequest(BaseModel):
    email: EmailStr
    token: str

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