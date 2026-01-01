#!/bin/bash
set -e

# Check if DATABASE_URL is set
if [ -z "$DATABASE_URL" ]; then
    echo "ERROR: DATABASE_URL environment variable is not set!"
    echo "Please configure DATABASE_URL in Railway project settings."
    exit 1
fi

# Run migrations
echo "Running database migrations..."
alembic upgrade head

# Start the server
echo "Starting FastAPI server on port ${PORT:-8000}..."
exec uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}

