from pydantic import BaseModel, EmailStr, Field, field_validator


# -------------------------------------------------
# REQUEST RESET
# -------------------------------------------------
class PasswordResetRequest(BaseModel):
    email: EmailStr = Field(..., description="Email do usuário para reset de senha")


# -------------------------------------------------
# CONFIRM RESET
# -------------------------------------------------
class PasswordResetConfirm(BaseModel):
    token: str = Field(..., min_length=10)
    new_password: str = Field(..., min_length=8)
    confirm_password: str = Field(..., min_length=8)

    @field_validator("new_password")
    @classmethod
    def validate_password_strength(cls, value: str) -> str:
        if not any(c.islower() for c in value):
            raise ValueError("A senha deve conter letra minúscula")

        if not any(c.isupper() for c in value):
            raise ValueError("A senha deve conter letra maiúscula")

        if not any(c.isdigit() for c in value):
            raise ValueError("A senha deve conter número")

        if not any(c in "!@#$%^&*()-_=+[]{}|;:,.<>?/" for c in value):
            raise ValueError("A senha deve conter caractere especial")

        return value

    @field_validator("confirm_password")
    @classmethod
    def validate_password_match(cls, confirm_value: str, info) -> str:
        password = info.data.get("new_password")

        if password and confirm_value != password:
            raise ValueError("As senhas não coincidem")

        return confirm_value
