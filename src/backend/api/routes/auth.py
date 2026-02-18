from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from slowapi import Limiter
from slowapi.util import get_remote_address

from backend.api.deps.database import get_db
from backend.api.schemas.user import UserLogin, Token
from backend.api.schemas.auth import (
    ActivateAccountRequest,
    SendActivationRequest,
)
from backend.api.schemas.password_reset import (
    PasswordResetRequest,
    PasswordResetConfirm,
)
from backend.api.services.auth_service import login_service

from backend.api.services.activation_token_service import ActivationTokenService
from backend.api.repositories.user_repository import UserRepository
from backend.api.core.auth import create_access_token
from backend.api.core.exceptions import (
    InvalidCredentialsError,
    InvalidActivationTokenError,
)
from backend.api.services.password_reset_service import PasswordResetService
from backend.api.core.mail.mail_service import MailService, get_mail_service
from backend.api.core.mail.mail_client_smtp import MailClientSMTP
import logging

# -------------------------------------------------
# Configuração do logger
# -------------------------------------------------
logger = logging.getLogger("auth_endpoints")
logger.setLevel(logging.INFO)

# -------------------------------------------------
# Limiter profissional
# -------------------------------------------------
limiter = Limiter(key_func=get_remote_address)

router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)

# ---------------------
# LOGIN
# ---------------------
@router.post("/login", response_model=Token)
@limiter.limit("5/minute")  # limitar tentativas de login
def login(
    request: Request,
    user_in: UserLogin,
    db: Session = Depends(get_db),
):
    try:
        return login_service(db, user_in.email, user_in.password)
    except InvalidCredentialsError as e:
        logger.warning(f"Login falhou para {user_in.email} - IP: {request.client.host}")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))

# ---------------------
# SEND ACTIVATION
# ---------------------
@router.post("/send-activation", status_code=status.HTTP_200_OK)
@limiter.limit("3/minute")  # 3 requisições por minuto por IP
def send_activation(
    request: Request,
    data: SendActivationRequest,
    db: Session = Depends(get_db),
):
    user_repo = UserRepository()
    user = user_repo.get_by_email(db, data.email)

    if not user:
        logger.info(f"Send activation attempted for unknown email: {data.email} - IP: {request.client.host}")
        return {"message": "Se o e-mail existir, um código de ativação foi enviado"}

    if user.is_active:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Conta já está ativa")

    mail_service = MailService(mail_client=MailClientSMTP())

    ActivationTokenService(db=db, mail_service=mail_service).create_activation_token(user)
    logger.info(f"Activation email sent to {data.email} - IP: {request.client.host}")

    return {"message": "Código de ativação enviado com sucesso"}

# ---------------------
# ACTIVATE ACCOUNT
# ---------------------
@router.post("/activate", status_code=status.HTTP_200_OK)
@limiter.limit("5/minute")
def activate_account(
    request: Request,
    data: ActivateAccountRequest,
    db: Session = Depends(get_db),
):
    try:
        ActivationTokenService(
            db=db,
        ).activate_account(
            email=data.email,
            token=data.token,
        )

        logger.info(
            f"Account activated for {data.email} - IP: {request.client.host}"
        )

    except InvalidActivationTokenError as e:
        logger.warning(
            f"Activation failed for {data.email}: {e} - IP: {request.client.host}"
        )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )

    return {"message": "Conta ativada com sucesso"}


# ---------------------
# PASSWORD RESET — REQUEST
# ---------------------
@router.post("/password-reset/request", status_code=status.HTTP_200_OK)
@limiter.limit("5/minute")  # 5 requisições por minuto por IP
def request_password_reset(
    request: Request,
    data: PasswordResetRequest,
    db: Session = Depends(get_db),
):
    PasswordResetService.request_reset(db=db, email=data.email)
    logger.info(f"Password reset requested for {data.email} - IP: {request.client.host}")
    return {"message": "Se o e-mail existir, um código de redefinição foi enviado"}

# ---------------------
# PASSWORD RESET — CONFIRM
# ---------------------
@router.post("/password-reset/confirm", status_code=status.HTTP_200_OK)
@limiter.limit("5/minute")  # 5 requisições por minuto por IP
def confirm_password_reset(
    request: Request,
    data: PasswordResetConfirm,
    db: Session = Depends(get_db),
):
    try:
        PasswordResetService.reset_password(
            db=db,
            token=data.token,
            new_password=data.new_password,
            confirm_password=data.confirm_password,
        )
        logger.info(f"Password reset confirmed - IP: {request.client.host}")
    except ValueError as e:
        logger.warning(f"Password reset failed: {e} - IP: {request.client.host}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    return {"message": "Senha redefinida com sucesso"}
