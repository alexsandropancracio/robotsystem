import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional

from backend.api.core.mail.mail_client import MailClient
from backend.api.core.config import get_settings


class MailClientSMTP(MailClient):
    """
    Cliente SMTP para envio de e-mails via servidor configurado.
    Implementa o contrato definido em MailClient.
    """

    def __init__(self) -> None:
        self.settings = get_settings()

        if not self.settings.SMTP_ENABLED:
            raise RuntimeError("SMTP está desabilitado nas configurações")

        required_settings = [
            self.settings.MAIL_HOST,
            self.settings.MAIL_PORT,
            self.settings.MAIL_FROM,
            self.settings.MAIL_USERNAME,
            self.settings.MAIL_PASSWORD,
        ]

        if not all(required_settings):
            raise RuntimeError("Configuração SMTP incompleta")

    def send(
        self,
        to: str,
        subject: str,
        html_body: str,
        text_body: Optional[str] = None,
    ) -> None:
        msg = MIMEMultipart("alternative")
        msg["From"] = self.settings.MAIL_FROM
        msg["To"] = to
        msg["Subject"] = subject

        # Fallback texto puro (opcional)
        if text_body:
            msg.attach(MIMEText(text_body, "plain", "utf-8"))

        # Corpo principal HTML
        msg.attach(MIMEText(html_body, "html", "utf-8"))

        try:
            with smtplib.SMTP(
                host=self.settings.MAIL_HOST,
                port=self.settings.MAIL_PORT,
                timeout=10,
            ) as server:

                if self.settings.MAIL_USE_TLS:
                    context = ssl.create_default_context()
                    server.starttls(context=context)

                server.login(
                    self.settings.MAIL_USERNAME,
                    self.settings.MAIL_PASSWORD,
                )

                server.sendmail(
                    self.settings.MAIL_FROM,
                    [to],
                    msg.as_string(),
                )

        except smtplib.SMTPException as exc:
            raise RuntimeError(
                f"Erro ao enviar e-mail via SMTP: {exc}"
            ) from exc
