uv run manage.py migrate
uv run manage.py collectstatic --noinput
uv run uvicorn app.asgi:application --host 0.0.0.0 --port 8000
