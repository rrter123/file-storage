#!/bin/sh

# Exit immediately if a command exits with a non-zero status
set -e

echo "Running database migrations..."
uv run manage.py migrate

echo "Starting server..."
exec uv run manage.py runserver 0.0.0.0:8000
