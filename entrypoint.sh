#!/bin/bash
set -e

# ==========================================
# 1. Start Redis Server (in daemon mode)
# ==========================================
echo "Starting Redis server..."
redis-server --daemonize yes

# Wait for Redis to be ready
until redis-cli ping | grep -q PONG; do
  echo "Waiting for Redis to start..."
  sleep 1
done
echo "Redis is up and running."

# ==========================================
# 2. Setup SQLite Database & Seed Data
# ==========================================
echo "Seeding the database..."
python seed.py

# ==========================================
# 3. Start Celery Worker & Scheduler
# ==========================================
echo "Starting Celery worker..."
celery -A app.jobs.tasks worker --loglevel=info &

echo "Starting Celery beat scheduler..."
celery -A app.jobs.tasks beat --loglevel=info &

# ==========================================
# 4. Start Flask backend via Gunicorn
# ==========================================
echo "Starting Gunicorn Flask server on port 7860..."
# Using exec to replace the shell process with gunicorn so Docker signals are handled properly
exec gunicorn -w 4 -b 0.0.0.0:7860 "run:app"
