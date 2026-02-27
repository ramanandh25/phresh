FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV UV_PROJECT_ENVIRONMENT=/usr/local

# System 
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    build-essential \
    libpq-dev \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

COPY pyproject.toml uv.lock alembic.ini ./

# Install dependencies
RUN uv sync --no-cache

# copy the rest of the application code
COPY backend ./backend
COPY tests ./tests

EXPOSE 8000

CMD ["uvicorn", "backend.app.api.server:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]