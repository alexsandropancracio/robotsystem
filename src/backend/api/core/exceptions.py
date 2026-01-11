# backend/api/core/exceptions.py

class UserAlreadyExistsError(Exception):
    pass

class InvalidCredentialsError(Exception):
    pass

class BusinessLogicError(Exception):
    """
    Erro base para regras de negócio previsíveis.
    Nunca deve virar 500.
    """

    status_code: int = 400
    detail: str = "Erro de regra de negócio"

    def __init__(self, detail: str | None = None):
        if detail:
            self.detail = detail
        super().__init__(self.detail)

class InvalidActivationTokenError(BusinessLogicError):
    status_code = 401
    detail = "Token de ativação inválido ou expirado"