# 1️⃣ Imagem base
FROM python:3.10-slim

# 2️⃣ Variáveis de ambiente para Python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# 3️⃣ Diretório de trabalho
WORKDIR /app

# 4️⃣ Dependências de sistema (para Postgres e compilação)
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# 5️⃣ Copiar requirements
COPY api/requirements.txt /app/requirements.txt

# 6️⃣ Instalar dependências Python
RUN pip install --upgrade pip && pip install -r requirements.txt

# 7️⃣ Copiar TODO o backend
COPY . /app

# 8️⃣ Expor porta
EXPOSE 8000

# 9️⃣ Comando padrão (pode ser sobrescrito pelo docker-compose)
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]

#APP_ENV=dev uvicorn backend.api.main:app --reload(pra rodar o swagger)

#docker compose -f docker-compose.dev.yml restart api

##alembic upgrade head

#container:
#docker compose -f docker-compose.dev.yml up -d --build (iniciar container)
#docker compose -f docker-compose.dev.yml build --no-cache
#docker compose -f docker-compose.dev.yml up -d
#docker compose -f docker-compose.dev.yml down (parar container)
#docker compose -f docker-compose.dev.yml exec api bash
#docker compose -f docker-compose.dev.yml exec postgres bash
#docker logs -f robotsystem-api-dev(log)

#banco de dados:
#psql -U user_dev -d robotsystem_dev

#limpar imagens do container:
#docker image prune -f
#docker system prune -f

#arquitetura do projeto:
#tree -I ".venv|__pycache__|.git"

#teste unitário
#pytest --cov=backend/api --cov-report=term-missing(linux/wls)
#pytest backend/tests \
  #--cov=backend/api \
  #--cov-report=term-missing

#pytest src/backend/tests --cov=src/backend/api --cov-report=term-missing
#pytest src/backend/tests `
  #--cov=src/backend/api `
  #--cov-report=term-missing

