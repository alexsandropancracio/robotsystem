import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from backend.api.core.config import get_settings

settings = get_settings()

class MailClientSMTP:
    """
    Cliente SMTP para envio de e-mails.
    Funciona com Gmail, Outlook e outros provedores que usam SMTP.
    """
    settings = get_settings()



    def __init__(self):
        if not settings.SMTP_ENABLED:
            raise RuntimeError("Configuração SMTP incompleta")

        self.host = settings.MAIL_HOST
        self.port = settings.MAIL_PORT
        self.username = settings.MAIL_USERNAME
        self.password = settings.MAIL_PASSWORD
        self.from_email = settings.MAIL_FROM
        self.use_tls = settings.MAIL_USE_TLS

    def send_email(self, to: str, subject: str, text: str, html: str = None) -> None:
        # Monta a mensagem
        msg = MIMEMultipart("alternative")
        msg["From"] = settings.MAIL_FROM
        msg["To"] = to
        msg["Subject"] = subject

        # Texto plano
        part_text = MIMEText(text, "plain")
        msg.attach(part_text)

        # HTML (opcional)
        if html:
            part_html = MIMEText(html, "html")
            msg.attach(part_html)

        # Conexão SMTP
        with smtplib.SMTP(self.host, self.port) as server:
            if self.use_tls:
                server.starttls()
            server.login(self.username, self.password)
            server.sendmail(self.username, to, msg.as_string())
