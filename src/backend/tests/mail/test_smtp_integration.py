import pytest

from backend.api.core.config import get_settings
from backend.api.core.mail.mail_service import MailService
from backend.api.core.mail.mail_client_smtp import MailClientSMTP


settings = get_settings()


@pytest.mark.skipif(
    not settings.SMTP_ENABLED,
    reason="SMTP não configurado no ambiente",
)
def test_send_password_reset_email_smtp():
    """
    Teste de integração SMTP.
    Verifica se o envio NÃO lança exceção.
    """

    client = MailClientSMTP()
    service = MailService(client)

    service.send_password_reset_email(
        email=settings.MAIL_FROM,  # envia pra você mesmo
        token="TOKEN_TESTE_SMTP",
        expires_in_minutes=30,
    )

@pytest.mark.skipif(
    not settings.SMTP_ENABLED,
    reason="SMTP não configurado no ambiente",
)
def test_smtp_send_email():
    """
    Teste de integração real com SMTP.
    Esse teste valida se o servidor SMTP está configurado corretamente
    e consegue enviar um e-mail.
    """

    client = MailClientSMTP()

    client.send(
        to=settings.MAIL_FROM,
        subject="Teste SMTP RobotSystem",
        html_body="<p><strong>Teste SMTP</strong> funcionando corretamente.</p>",
        text_body="Este é um teste de envio de e-mail via SMTP no RobotSystem.",
    )

