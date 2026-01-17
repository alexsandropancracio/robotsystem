# src/backend/tests/mail/test_send_real_email.py
import pytest
from backend.api.core.mail.mail_client_smtp import MailClientSMTP
from backend.api.core.mail.mail_service import MailService

#@pytest.mark.skip(reason="Testando envio real de e-mail")
def test_send_activation_email_real():
    client = MailClientSMTP()
    service = MailService(client)

    service.send_activation_email(
        email="alexsandropancracioofficial@gmail.com",  # e-mail de teste
        token="123456",  # token de teste
    )

    # Se não der erro, passou
    assert True
