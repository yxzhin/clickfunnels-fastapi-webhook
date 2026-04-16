#!/bin/sh
set -e

exec uv run fastapi dev src/backend/app/main.py --host 0.0.0.0 --port 8000
