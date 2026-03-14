# Use the Python 3.14 slim image
FROM python:3.14-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

# Python 3.14 optimization: 
# Pre-compiling bytecode is even more effective now.
ENV UV_COMPILE_BYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --no-install-project

COPY . .
RUN uv sync --frozen --no-dev

ENV PATH="/app/.venv/bin:$PATH"

CMD ["streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0"]