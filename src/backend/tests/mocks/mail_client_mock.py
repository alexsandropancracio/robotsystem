class MailClientMock:
    def __init__(self):
        self.sent_emails = []

    def send_email(
        self,
        *,
        to: str,
        subject: str,
        text: str,
        html: str,
    ) -> None:
        self.sent_emails.append(
            {
                "to": to,
                "subject": subject,
                "text": text,
                "html": html,
            }
        )
