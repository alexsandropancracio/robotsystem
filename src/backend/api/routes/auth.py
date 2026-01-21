from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.api.deps.database import get_db
from backend.api.models.user import User
from backend.api.schemas.user import UserLogin, Token
from backend.api.schemas.auth import (
    ActivateAccountRequest,
    SendActivationRequest,
    RefreshTokenRequest,
)
from backend.api.services.auth_service import login_service
from backend.api.services.refresh_token_service import RefreshTokenService
from backend.api.services.activation_token_service import ActivationTokenService
from backend.api.repositories.user_repository import UserRepository
from backend.api.core.auth import create_access_token
from backend.api.core.exceptions import (
    InvalidCredentialsError,
    InvalidActivationTokenError,
)
from backend.api.schemas.password_reset import (
    PasswordResetRequest,
    PasswordResetConfirm,
)
from backend.api.services.password_reset_service import PasswordResetService


router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)

# -------------------------------------------------
# LOGIN
# -------------------------------------------------
@router.post("/login", response_model=Token)
def login(
    user_in: UserLogin,
    db: Session = Depends(get_db),
):
    try:
        return login_service(
            db,
            user_in.email,
            user_in.password,
        )

    except InvalidCredentialsError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
        )


# -------------------------------------------------
# LOGOUT
# -------------------------------------------------
@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(
    data: RefreshTokenRequest,
    db: Session = Depends(get_db),
):
    refresh_service = RefreshTokenService(db)

    revoked = refresh_service.revoke_refresh_token(data.refresh_token)
    if not revoked:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Refresh token inválido ou já revogado",
        )


# -------------------------------------------------
# REFRESH TOKEN
# -------------------------------------------------
@router.post("/refresh", response_model=Token)
def refresh_token(
    data: RefreshTokenRequest,
    db: Session = Depends(get_db),
):
    refresh_service = RefreshTokenService(db)

    result = refresh_service.rotate_refresh_token(data.refresh_token)

    if not result:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token inválido ou expirado",
        )

    user, new_refresh_token = result

    access_token = create_access_token(
        {"sub": str(user.id)}
    )

    return Token(
        access_token=access_token,
        refresh_token=new_refresh_token,
    )


# -------------------------------------------------
# ATIVAÇÃO DE CONTA
# -------------------------------------------------
@router.post("/activate", status_code=status.HTTP_200_OK)
def activate_account(
    data: ActivateAccountRequest,
    db: Session = Depends(get_db),
):
    """
    Ativa a conta do usuário usando o token de 6 dígitos enviado por e-mail.
    """
    service = ActivationTokenService(db)

    try:
        service.activate_account(
            email=data.email,
            token=data.token,
        )
    except InvalidActivationTokenError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Token inválido ou expirado",
        )

    return {
        "message": "Conta ativada com sucesso"
    }


# -------------------------------------------------
# ENVIO DE TOKEN DE ATIVAÇÃO
# -------------------------------------------------
@router.post("/send-activation", status_code=status.HTTP_200_OK)
def send_activation(
    data: SendActivationRequest,
    db: Session = Depends(get_db),
):
    """
    Envia um token de ativação para o e-mail do usuário.
    """
    user_repo = UserRepository()
    user = user_repo.get_by_email(db, data.email)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Não foi possível enviar o código de ativação",
        )

    if user.is_active:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Conta já está ativa",
        )

    token = ActivationTokenService(db).create_activation_token(user)

    return {
        "message": "Código de ativação enviado com sucesso",
        # ⚠️ DEV ONLY — remover quando o envio de e-mail estiver ativo
        "activation_token": token,
    }

# -------------------------------------------------
# PASSWORD RESET — REQUEST
# -------------------------------------------------
@router.post(
    "/password-reset/request",
    status_code=status.HTTP_200_OK,
)
def request_password_reset(
    data: PasswordResetRequest,
    db: Session = Depends(get_db),
):
    """
    Solicita redefinição de senha.
    Sempre retorna sucesso (anti-enumeração).
    """
    PasswordResetService.request_reset(
        db=db,
        email=data.email,
    )

    return {
        "message": "Se o e-mail existir, um código de redefinição foi enviado"
    }

# -------------------------------------------------
# PASSWORD RESET — CONFIRM
# -------------------------------------------------
@router.post(
    "/password-reset/confirm",
    status_code=status.HTTP_200_OK,
)
def confirm_password_reset(
    data: PasswordResetConfirm,
    db: Session = Depends(get_db),
):
    """
    Confirma redefinição de senha usando token.
    """
    try:
        PasswordResetService.reset_password(
            db=db,
            token=data.token,
            new_password=data.new_password,
            confirm_password=data.confirm_password,
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )

    return {
        "message": "Senha redefinida com sucesso"
    }
