from datetime import datetime, timedelta
import pytest

from backend.api.services.activation_token_service import ActivationTokenService
from backend.api.core.exceptions import InvalidActivationTokenError
from backend.api.models.activation_token import ActivationToken
from backend.api.core.security.token import hash_token
from backend.tests.factories.user_factory import create_user

def test_create_activation_token(db_session):
    user = create_user()
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    service = ActivationTokenService(db_session)
    token = service.create_activation_token(user)

    assert token is not None
    assert len(token) == 6

def test_create_activation_token_for_active_user_raises_error(db_session):
    user = create_user(is_active=True)
    db_session.add(user)
    db_session.commit()

    service = ActivationTokenService(db_session)

    with pytest.raises(InvalidActivationTokenError):
        service.create_activation_token(user)

def test_activate_user_with_valid_token(db_session):
    user = create_user()
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    service = ActivationTokenService(db_session)
    token = service.create_activation_token(user)

    service.activate_account(
        email=user.email,
        token=token,
    )

    db_session.refresh(user)
    assert user.is_active is True
    assert user.is_email_verified is True

def test_activate_user_with_invalid_token(db_session):
    user = create_user()
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    service = ActivationTokenService(db_session)
    service.create_activation_token(user)

    with pytest.raises(InvalidActivationTokenError):
        service.activate_account(
            email=user.email,
            token="000000",
        )

def test_activation_token_cannot_be_reused(db_session):
    user = create_user()
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    service = ActivationTokenService(db_session)
    token = service.create_activation_token(user)

    service.activate_account(
        email=user.email,
        token=token,
    )

    with pytest.raises(InvalidActivationTokenError):
        service.activate_account(
            email=user.email,
            token=token,
        )


def test_create_activation_token(db_session, user_factory):
    user = user_factory(is_active=False)
    service = ActivationTokenService(db_session)

    token = service.create_activation_token(user)

    assert token is not None
    assert len(token) == 6


def test_cannot_activate_already_active_user(db_session, user_factory):
    user = user_factory(is_active=True)
    service = ActivationTokenService(db_session)

    with pytest.raises(InvalidActivationTokenError):
        service.create_activation_token(user)

def test_cannot_activate_with_expired_token(db_session, user_factory):
    user = user_factory(is_active=False)
    service = ActivationTokenService(db_session)

    # cria token expirado manualmente
    expired_token = ActivationToken(
        user_id=user.id,
        token="123456",
        expires_at=datetime.utcnow() - timedelta(minutes=1),
        is_used=False,
    )

    db_session.add(expired_token)
    db_session.commit()

    with pytest.raises(InvalidActivationTokenError):
        service.activate_user(
            user=user,
            token="123456",
        )