uv run manage.py migrate
uv run uvicorn app.asgi:application --host 0.0.0.0 --port ${PORT:-8000}
