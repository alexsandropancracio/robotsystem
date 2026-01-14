from backend.api.core.mail.mail_service import MailService
from backend.tests.mocks.mail_client_mock import MailClientMock


def test_send_activation_email_sends_email_correctly():
    client = MailClientMock()
    service = MailService(client)

    service.send_activation_email(
        email="test@example.com",
        token="123456",
    )

    assert len(client.sent_emails) == 1

    sent = client.sent_emails[0]

    assert sent["to"] == "test@example.com"
    assert "123456" in sent["text"]
    assert "123456" in sent["html"]
    assert sent["subject"]
