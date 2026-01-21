from backend.api.core.mail.mail_service import MailService
from backend.tests.mocks.mail_client_mock import MailClientMock


def test_send_password_reset_email():
    client = MailClientMock()
    service = MailService(client)

    email = "user@test.com"
    token = "RESET123"
    expires = 30

    service.send_password_reset_email(
        email=email,
        token=token,
        expires_in_minutes=expires,
    )

    assert client.count == 1

    last = client.last_email
    assert last is not None
    assert last["to"] == email
    assert "Recuperação de senha" in last["subject"]
    assert token in last["text"]
    assert token in last["html"]

