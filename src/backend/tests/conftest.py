import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from backend.api.main import app
from backend.api.database.base import Base
from backend.api.database.session import get_db
from backend.api.models.user import User
from backend.api.models.password_reset_token import PasswordResetToken


@pytest.fixture
def db_session():
    engine = create_engine("sqlite:///:memory:")
    TestingSessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine,
    )

    Base.metadata.create_all(bind=engine)

    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as client:
        yield client

    app.dependency_overrides.clear()


@pytest.fixture
def user_factory(db_session):
    def _factory(**kwargs):
        user = User(
            email=kwargs.get("email", "test@example.com"),
            hashed_password=kwargs.get("hashed_password", "fake-hash"),
            is_active=kwargs.get("is_active", True),
            is_email_verified=kwargs.get("is_email_verified", True),
        )
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)
        return user

    return _factory
