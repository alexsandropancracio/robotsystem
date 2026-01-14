from backend.api.core.mail.mail_templates import activation_email_template
from backend.api.core.mail.mail_client import MailClient
from backend.api.core.config import get_settings

settings = get_settings()


class MailService:

    def __init__(self, client: MailClient):
        self.client = client

    def send_activation_email(
        self,
        email: str,
        token: str,
        expires_in_minutes: int | None = None,
    ) -> None:

        subject, text, html = activation_email_template(
            user_email=email,
            activation_token=token,
        )

        self.client.send_email(
            to=email,
            subject=subject,
            text=text,
            html=html,
        )
