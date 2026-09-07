FROM python:3.14-slim

# Install uv from official image
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

ENV UV_COMPILE_BYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Cache dependencies layer
COPY pyproject.toml .
RUN uv venv .venv --python 3.14 && \
    uv pip install --python .venv -r pyproject.toml

# Copy project source
COPY . .

# Install project package into venv without re-downloading dependencies
RUN uv pip install --python .venv --no-deps .

ENV PATH="/app/.venv/bin:$PATH"

EXPOSE 5000

CMD ["python", "-u", "main.py"]
