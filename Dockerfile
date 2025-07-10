FROM python:3.10-slim

RUN mkdir /app
WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1 

# Install UV
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Install dependencies
COPY pyproject.toml uv.lock /app/
RUN uv sync --locked

# Do not run as root
RUN useradd -m -r appuser && \
    chown -R appuser /app

# Copy application code
COPY --chown=appuser:appuser devfest_lecce_2025_be/ ./

# Switch to non-root user
USER appuser

# Expose the application port
EXPOSE 8000 

# Run with uvicorn
CMD ["bash", "run.sh"]
