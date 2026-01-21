from abc import ABC, abstractmethod


class MailClient(ABC):
    """
    Interface base para clientes de e-mail.

    Contrato:
    - html_body é o corpo principal do e-mail
    - text_body é fallback para clientes que não suportam HTML
    """

    @abstractmethod
    def send(
        self,
        to: str,
        subject: str,
        html_body: str,
        text_body: str | None = None,
    ) -> None:
        """
        Envia um e-mail.

        :param to: Destinatário
        :param subject: Assunto do e-mail
        :param html_body: Corpo principal em HTML
        :param text_body: Corpo alternativo em texto puro (opcional)
        """
        raise NotImplementedError
