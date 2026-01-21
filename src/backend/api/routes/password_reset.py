from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.api.schemas.password_reset import (
    PasswordResetRequest,
    PasswordResetConfirm,
)
from backend.api.services.password_reset_service import PasswordResetService
from backend.api.database.session import get_db
from backend.api.core.mail.mail_client_smtp import MailClientSMTP
from backend.api.core.mail.mail_service import MailService


router = APIRouter(
    prefix="/auth/password-reset",
    tags=["Auth - Password Reset"],
)


# -------------------------------------------------
# REQUEST PASSWORD RESET (envia email)
# -------------------------------------------------
@router.post(
    "/request",
    status_code=status.HTTP_204_NO_CONTENT,
)
def request_password_reset(
    payload: PasswordResetRequest,
    db: Session = Depends(get_db),
) -> None:
    """
    Solicita reset de senha.
    Sempre retorna 204 para evitar enumeração de usuários.
    """
    try:
        mail_client = MailClientSMTP()
        mail_service = MailService(mail_client)
        service = PasswordResetService(mail_service)

        service.request_reset(
            db=db,
            email=payload.email,
        )

    except Exception:
        # Anti-enumeração: nunca expõe erro
        pass


# -------------------------------------------------
# CONFIRM PASSWORD RESET (troca a senha)
# -------------------------------------------------
@router.post(
    "/confirm",
    status_code=status.HTTP_204_NO_CONTENT,
)
def confirm_password_reset(
    payload: PasswordResetConfirm,
    db: Session = Depends(get_db),
) -> None:
    """
    Confirma reset de senha usando token válido.
    """
    try:
        mail_client = MailClientSMTP()
        mail_service = MailService(mail_client)
        service = PasswordResetService(mail_service)

        service.reset_password(
            db=db,
            token=payload.token,
            new_password=payload.new_password,
            confirm_password=payload.confirm_password,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )
