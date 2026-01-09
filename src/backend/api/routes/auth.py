# backend/api/routes/auth.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.api.deps.database import get_db
from backend.api.schemas.auth import (
    LoginRequest,
    TokenResponse,
    RefreshTokenRequest,
)
#from backend.api.services.auth_services import authenticate_user
from backend.api.services.refresh_token_service import RefreshTokenService
from backend.api.core.security import create_access_token
from backend.api.core.exceptions import InvalidCredentialsError
from backend.api.services import user_service
from backend.api.schemas.user import UserLogin, Token

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
    """
    Login do usuário
    """
    try:
        return user_service.login_user_service(db, user_in)
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
    """
    Revoga explicitamente um refresh token.
    """
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
@router.post("/refresh", response_model=TokenResponse)
def refresh_token(
    data: RefreshTokenRequest,
    db: Session = Depends(get_db),
):
    """
    Rotaciona refresh token:
    - valida token atual
    - revoga o antigo
    - cria um novo
    - gera novo access token
    """
    refresh_service = RefreshTokenService(db)

    new_refresh = refresh_service.rotate_refresh_token(data.refresh_token)
    if not new_refresh:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token inválido ou expirado",
        )

    access_token = create_access_token(
        subject=str(new_refresh.user.id)
    )

    return TokenResponse(
        access_token=access_token,
        refresh_token=new_refresh.token,
        token_type="bearer",
    )
