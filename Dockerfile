FROM python:3.12-slim AS builder

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1 
ENV UV_PROJECT_ENVIRONMENT=/usr/local



RUN apt-get update \
    && apt-get -y install --no-install-recommends \
    gcc postgresql \
    build-essential \
    libpq-dev  \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

COPY pyproject.toml uv.lock alembic.ini  ./

RUN  uv sync --no-cache

COPY backend ./backend

EXPOSE 8000

# Start FastAPI
CMD ["uvicorn", "backend.app.api.server:app", "--host", "0.0.0.0", "--port", "8000"]

