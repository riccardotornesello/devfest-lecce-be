#!/bin/bash

if [ "$TASK" == "collectstatic" ]; then
    echo "Collecting static files..."
    uv run manage.py collectstatic --noinput

elif [ "$TASK" == "migrate" ]; then
    echo "Applying migrations..."
    uv run manage.py migrate

elif [ "$TASK" == "" ]; then
    echo "Starting the application..."
    uv run uvicorn app.asgi:application --host 0.0.0.0 --port ${PORT:-8000}

else
    echo "Unknown task: $TASK"
    exit 1

fi
