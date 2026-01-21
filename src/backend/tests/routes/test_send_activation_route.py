# tests/routes/test_send_activation_route.py
import pytest
from fastapi.testclient import TestClient
from backend.api.main import app
from backend.tests.mocks.mail_client_mock import MailClientMock
from backend.api.services.activation_token_service import ActivationTokenService
from backend.api.core.mail.mail_service import MailService
from backend.tests.factories.user_factory import create_user
from backend.api.deps.database import get_db

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def mail_service_mock():
    return MailService(mail_client=MailClientMock())

@pytest.fixture
def test_user(db=pytest.lazy_fixture("get_db")):
    # Cria usuário de teste com factory
    return create_user(db, email="teste@robotsystem.com", password="12345678")

def test_send_activation(client, test_user, mail_service_mock, db):
    """
    Testa o endpoint /auth/send-activation.
    """

    # Substituir o ActivationTokenService do endpoint pelo mock
    ActivationTokenService(db=db, mail_service=mail_service_mock).create_activation_token(test_user)

    response = client.post(
        "/auth/send-activation",
        json={"email": test_user.email}
    )

    assert response.status_code == 200
    assert "message" in response.json()
    # Checa se o e-mail foi "enviado" via mock
    assert mail_service_mock.sent_emails
    assert mail_service_mock.sent_emails[0]["to"] == test_user.email
