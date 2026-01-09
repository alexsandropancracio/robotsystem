class AuthService:
    def __init__(self, user_repo):
        self.user_repo = user_repo

    def register(self, username: str, password: str):
        return self.user_repo.create_user(username, password)

    def login(self, username: str, password: str):
        return self.user_repo.authenticate(username, password)
