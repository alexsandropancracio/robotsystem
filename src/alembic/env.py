# alembic/env.py
import os
from pathlib import Path
from dotenv import load_dotenv
from logging.config import fileConfig

from sqlalchemy import create_engine, pool
from alembic import context

from backend.api.database.base import Base
import backend.api.models  # garante que todos os models sejam carregados
from backend.api.core.config import get_settings

import sys
from pathlib import Path

# -------------------------------
# BASE_DIR do projeto
# -------------------------------
BASE_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(BASE_DIR))

# -------------------------------
# Escolher o .env correto
# -------------------------------
ENV = os.getenv("ENV", "dev").lower()

env_file_map = {
    "dev": BASE_DIR / "backend" / ".env.dev",
    "prod": BASE_DIR / "backend" / ".env.prod",
}

env_path = env_file_map.get(ENV)

if env_path and env_path.exists():
    load_dotenv(env_path, encoding="utf-8")
    print(f"✅ Alembic carregou env: {env_path}")
else:
    raise RuntimeError(
        f"❌ Arquivo de ambiente não encontrado para ENV={ENV}: {env_path}"
    )

# -------------------------------
# Alembic Config
# -------------------------------
config = context.config

# Logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

settings = get_settings()

config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

# Metadata que Alembic vai usar
target_metadata = Base.metadata

# -------------------------------
# Função de migração offline
# -------------------------------
def run_migrations_offline() -> None:
    settings = get_settings()
    url = settings.DATABASE_URL

    context.configure(
        url=url,
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
    settings = get_settings()

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
# Executar migração de acordo com o modo
# -------------------------------
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()