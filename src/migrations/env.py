# migrations/env.py
import os
import sys
from pathlib import Path
from logging.config import fileConfig

from alembic import context
from sqlalchemy import create_engine, pool
from dotenv import load_dotenv

# -------------------------------
# BASE_DIR e sys.path (PRIMEIRO)
# -------------------------------
BASE_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(BASE_DIR))

# -------------------------------
# Imports do projeto
# -------------------------------
from backend.api.database.base import Base
from backend.api.core.config import get_settings

# IMPORTA OS MODELS AQUI 👇 (EXPLÍCITO)
from backend.api.models.user import User
from backend.api.models.license import License
from backend.api.models.refresh_token import RefreshToken
from backend.api.models.activation_token import ActivationToken

# Metadata que Alembic vai usar
target_metadata = Base.metadata

# -------------------------------
# Escolher o .env correto
# -------------------------------
ENV = os.getenv("ENV", "dev").lower()

env_file_map = {
    "dev": BASE_DIR / "backend" / ".env.dev",
    "prod": BASE_DIR / "backend" / ".env.prod",
}

env_path = env_file_map.get(ENV)

if not env_path or not env_path.exists():
    raise RuntimeError(
        f"❌ Arquivo de ambiente não encontrado para ENV={ENV}: {env_path}"
    )

load_dotenv(env_path, encoding="utf-8")
print(f"✅ Alembic carregou env: {env_path}")

# -------------------------------
# Alembic Config
# -------------------------------
config = context.config

if config.config_file_name:
    fileConfig(config.config_file_name)

settings = get_settings()
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

# -------------------------------
# Função de migração offline
# -------------------------------
def run_migrations_offline() -> None:
    context.configure(
        url=settings.DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()

# -------------------------------
# Função de migração online
# -------------------------------
def run_migrations_online() -> None:
    connectable = create_engine(
        settings.DATABASE_URL,
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
        )

        with context.begin_transaction():
            context.run_migrations()

# -------------------------------
# Executar migração
# -------------------------------
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
