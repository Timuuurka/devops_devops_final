#!/usr/bin/env sh
set -e

echo "[entrypoint] Initializing database (create_all + seed)..."
python init_db.py

echo "[entrypoint] Starting gunicorn..."
exec gunicorn -w 2 -b 0.0.0.0:5000 wsgi:app
