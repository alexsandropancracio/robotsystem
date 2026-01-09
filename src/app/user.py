# app/repositories/user.py

class UserRepository:
    def __init__(self, db=None):
        """
        Repositório de Usuário.
        Por enquanto db é opcional, pois não temos banco real configurado.
        """
        self.db = db  # mantém referência futura
        
    def create_user(self, username: str, password: str):
        """
        Criar usuário (placeholder até ter BD)
        """
        # ⚠️ Futuro: salvar no banco
        print(f"[UserRepository] create_user chamado: {username=}, {password=}")
        return {"status": "ok", "msg": "usuário registrado (fake)"}

    def authenticate(self, username: str, password: str):
        """
        Autenticar usuário (simulação)
        """
        print(f"[UserRepository] authenticate chamado: {username=}, {password=}")
        # ⚠️ apenas placeholder até login real
        if username == "admin" and password == "admin":
            return {"status": "ok", "msg": "login bem-sucedido!"}
        return {"status": "erro", "msg": "usuário ou senha incorretos"}
