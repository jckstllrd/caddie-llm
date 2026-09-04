FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_CACHE_DIR=/tmp/uv-cache

RUN useradd -m app && mkdir -p /usr/local/app && chown -R app:app /usr/local/app

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /usr/local/app
USER app

COPY pyproject.toml uv.lock* ./
RUN uv sync --frozen --no-dev

COPY app ./app

CMD ["uv", "run", "fastapi", "run", "app/main.py", "--host", "0.0.0.0", "--port", "8080"]
