from backend.api.core.mail.mail_templates import (
    activation_email_template,
    password_reset_email_template,
)
from backend.api.core.mail.mail_client import MailClient
from backend.api.core.config import settings


class MailService:
    def __init__(self, client: MailClient):
        self.client = client

    # -------------------------------------------------
    # ATIVAÇÃO DE CONTA
    # -------------------------------------------------
    def send_activation_email(
        self,
        email: str,
        token: str,
        expires_in_minutes: int | None = None,
    ) -> None:
        subject, text, html = activation_email_template(
            user_email=email,
            activation_token=token,
            expires_in_minutes=expires_in_minutes,
        )

        self.client.send(
            to=email,
            subject=subject,
            html_body=html,
            text_body=text,
        )

    # -------------------------------------------------
    # RESET DE SENHA
    # -------------------------------------------------
    def send_password_reset_email(
        self,
        email: str,
        token: str,
        expires_in_minutes: int | None = None,
    ) -> None:
        subject, text, html = password_reset_email_template(
            user_email=email,
            reset_token=token,
            expires_in_minutes=expires_in_minutes,
        )

        self.client.send(
            to=email,
            subject=subject,
            html_body=html,
            text_body=text,
        )


# -------------------------------------------------
# DEPENDENCY PROVIDER (FastAPI)
# -------------------------------------------------
def get_mail_service() -> MailService:
    client = MailClient(
        host=settings.SMTP_HOST,
        port=settings.SMTP_PORT,
        username=settings.SMTP_USER,
        password=settings.SMTP_PASSWORD,
        use_tls=settings.SMTP_USE_TLS,
    )
    return MailService(client=client)
