from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache
from pathlib import Path
from dotenv import load_dotenv
import os

# Raiz do projeto (src/backend)
BASE_DIR = Path(__file__).resolve().parents[2]

# Ambiente da aplicação
APP_ENV = os.getenv("APP_ENV", "dev").lower()

if APP_ENV not in ("dev", "prod"):
    raise RuntimeError(f"APP_ENV inválido: {APP_ENV}")

# Mapeamento correto de envs
ENV_FILE_MAP = {
    "dev": BASE_DIR / ".env.dev",
    "prod": BASE_DIR / ".env.prod",
}

env_file = ENV_FILE_MAP[APP_ENV]

# Carrega dotenv manualmente
if env_file.exists():
    load_dotenv(env_file, override=False)


class Settings(BaseSettings):
    ENV: str = APP_ENV
    DEBUG: bool = APP_ENV == "dev"

    API_NAME: str = "RobotSystem API"
    API_VERSION: str = "1.0.0"

    SECRET_KEY: str
    PEPPER: str
    ALGORITHM: str = "HS256"

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    MAX_REFRESH_TOKENS_PER_USER: int = 3

    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_DB: str

    EMAIL_GMAIL_USER: str | None = None
    EMAIL_GMAIL_PASS: str | None = None
    EMAIL_OUTLOOK_USER: str | None = None
    EMAIL_OUTLOOK_PASS: str | None = None

    @property
    def DATABASE_URL(self) -> str:
        return (
            f"postgresql+psycopg2://"
            f"{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    model_config = SettingsConfigDict(
        env_file=None,  # dotenv já cuidou disso
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
