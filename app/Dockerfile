# pull official base image
FROM python:3.14-trixie

# set work directory
WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_LINK_MODE=copy \
    UV_PYTHON_DOWNLOADS=never \
    UV_PROJECT_ENVIRONMENT=/app/.venv

# install uv
COPY --from=ghcr.io/astral-sh/uv:0.12.9 /uv /uvx /bin/

# 1. Copy package files first
COPY pyproject.toml uv.lock ./

# 2. Install dependencies (cached layer)
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync \
    --frozen \
    --no-install-project

# 3. Copy ONLY the contents of your app folder into /app
# This merges your source code safely without overriding pyproject.toml or uv.lock
COPY app/ ./

# Make the script executable
RUN chmod +x ./entrypoint.sh

# Run the script when the container starts
ENTRYPOINT ["./entrypoint.sh"]
