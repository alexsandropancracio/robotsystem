from app.interface import get_auth_service

class WebviewAPI:
    def __init__(self, window):
        self.window = window
        self.auth = get_auth_service()

    def login(self, email, senha):
        return self.auth.login(email, senha)

    def register(self, email, senha):
        return self.auth.register(email, senha)
