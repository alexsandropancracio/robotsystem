import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from backend.api.main import app
from backend.api.database.base import Base
from backend.api.database.session import get_db
from backend.api.models.user import User
from backend.api.core.mail.mail_service import MailService
from backend.tests.mocks.mail_client_mock import MailClientMock
from backend.api.core.mail.mail_service import get_mail_service


# ------------------------------
# Engine global
# ------------------------------
engine = create_engine(
    "sqlite:///:memory:",
    connect_args={"check_same_thread": False},
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

# ------------------------------
# DB fixture
# ------------------------------
@pytest.fixture
def db_session():
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)

# ------------------------------
# Mail mock fixture
# ------------------------------
@pytest.fixture
def mail_client_mock():
    return MailClientMock()
@pytest.fixture
def mail_service_mock():
    client = MailClientMock()
    service = MailService(client)
    return service

# ------------------------------
# Client fixture
# ------------------------------
@pytest.fixture
def client(db_session, mail_service_mock):
    def override_get_db():
        yield db_session

    def override_mail_service():
        return mail_service_mock

    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[MailService] = override_mail_service

    with TestClient(app) as client:
        yield client

    app.dependency_overrides.clear()

# ------------------------------
# User factory
# ------------------------------
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
