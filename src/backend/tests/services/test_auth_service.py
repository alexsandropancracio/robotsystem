import pytest

from backend.api.services.auth_service import (
    authenticate_user,
    login_service,
)
from backend.api.core.auth import hash_password
from backend.api.core.exceptions import InvalidCredentialsError
from backend.api.models.user import User


# -------------------------------------------------
# Fixtures auxiliares
# -------------------------------------------------
@pytest.fixture
def active_user(db_session):
    user = User(
        email="auth@test.com",
        hashed_password=hash_password("Senha@123"),
        is_active=True,
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def inactive_user(db_session):
    user = User(
        email="inactive@test.com",
        hashed_password=hash_password("Senha@123"),
        is_active=False,
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


# -------------------------------------------------
# authenticate_user
# -------------------------------------------------
def test_authenticate_user_success(db_session, active_user):
    user = authenticate_user(
        db=db_session,
        email=active_user.email,
        password="Senha@123",
    )

    assert user.id == active_user.id
    assert user.email == active_user.email


def test_authenticate_user_wrong_password(db_session, active_user):
    with pytest.raises(InvalidCredentialsError):
        authenticate_user(
            db=db_session,
            email=active_user.email,
            password="SenhaErrada@123",
        )


def test_authenticate_user_not_found(db_session):
    with pytest.raises(InvalidCredentialsError):
        authenticate_user(
            db=db_session,
            email="naoexiste@test.com",
            password="Senha@123",
        )


def test_authenticate_user_inactive(db_session, inactive_user):
    with pytest.raises(InvalidCredentialsError):
        authenticate_user(
            db=db_session,
            email=inactive_user.email,
            password="Senha@123",
        )


# -------------------------------------------------
# login_service
# -------------------------------------------------
def test_login_service_success(db_session, active_user):
    result = login_service(
        db=db_session,
        email=active_user.email,
        password="Senha@123",
    )

    assert "access_token" in result
    assert "refresh_token" in result
    assert result["token_type"] == "bearer"
