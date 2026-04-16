#!/bin/sh
set -e

exec /app/.venv/bin/gunicorn src.backend.app.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
