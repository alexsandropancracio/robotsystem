from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache
from pathlib import Path
from dotenv import load_dotenv
import os

# =================================================
# BASE DO PROJETO
# =================================================

# Raiz do projeto (src/backend)
BASE_DIR = Path(__file__).resolve().parents[2]

# =================================================
# AMBIENTE
# =================================================

APP_ENV = os.getenv("APP_ENV", "dev").lower()

if APP_ENV not in ("dev", "prod"):
    raise RuntimeError(f"APP_ENV inválido: {APP_ENV}")

ENV_FILE_MAP = {
    "dev": BASE_DIR / ".env.dev",
    "prod": BASE_DIR / ".env.prod",
}

env_file = ENV_FILE_MAP[APP_ENV]

# Carrega dotenv manualmente (controlado)
if env_file.exists():
    load_dotenv(env_file, override=False)

# =================================================
# SETTINGS
# =================================================

class Settings(BaseSettings):
    # -------------------------
    # APP
    # -------------------------
    ENV: str = APP_ENV
    DEBUG: bool = APP_ENV == "dev"

    API_NAME: str = "RobotSystem API"
    API_VERSION: str = "1.0.0"

    # -------------------------
    # SEGURANÇA
    # -------------------------
    SECRET_KEY: str
    PEPPER: str
    ALGORITHM: str = "HS256"

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7
    MAX_REFRESH_TOKENS_PER_USER: int = 3

    # -------------------------
    # DATABASE
    # -------------------------
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_DB: str

    # -------------------------
    # EMAIL (LEGADO / FUTURO)
    # -------------------------
    # Mantidos caso futuramente queira múltiplos emissores
    EMAIL_GMAIL_USER: str | None = None
    EMAIL_GMAIL_PASS: str | None = None
    EMAIL_OUTLOOK_USER: str | None = None
    EMAIL_OUTLOOK_PASS: str | None = None

    # -------------------------
    # SMTP (ENVIO DE E-MAIL)
    # -------------------------
    MAIL_HOST: str | None = None
    MAIL_PORT: int | None = None
    MAIL_USERNAME: str | None = None
    MAIL_PASSWORD: str | None = None
    MAIL_FROM: str | None = None

    MAIL_USE_TLS: bool = True
    MAIL_USE_SSL: bool = False

    # =================================================
    # PROPERTIES
    # =================================================

    @property
    def DATABASE_URL(self) -> str:
        return (
            f"postgresql+psycopg2://"
            f"{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}"
            f"/{self.POSTGRES_DB}"
        )

    @property
    def SMTP_ENABLED(self) -> bool:
        """
        Indica se o SMTP está corretamente configurado
        """
        return all(
            [
                self.MAIL_HOST,
                self.MAIL_PORT,
                self.MAIL_USERNAME,
                self.MAIL_PASSWORD,
                self.MAIL_FROM,
            ]
        )

    # =================================================
    # Pydantic config
    # =================================================
    model_config = SettingsConfigDict(
        env_file=None,     # dotenv já foi carregado manualmente
        extra="ignore",    # ignora variáveis extras no .env
        case_sensitive=True,
    )

# =================================================
# SINGLETON
# =================================================

@lru_cache
def get_settings() -> Settings:
    return Settings()

# -------------------------------------------------
# Instância global (usada via import)
# -------------------------------------------------
settings = get_settings()