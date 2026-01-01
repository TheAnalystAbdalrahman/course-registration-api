#!/bin/bash
# Don't exit on error - we want the server to start even if migrations fail
set +e

# Ensure output is unbuffered - Railway needs to see logs immediately
export PYTHONUNBUFFERED=1

# Get port from environment or default to 8000
PORT=${PORT:-8000}

echo "=========================================="
echo "Starting Course Registration API"
echo "Server will listen on port: $PORT"
echo "=========================================="

# Run migrations (non-blocking - failures won't stop the server)
echo "Running database migrations..."
alembic upgrade head || echo "WARNING: Migrations failed, but continuing startup..."

# Start the server
echo "Starting FastAPI server on 0.0.0.0:$PORT..."
echo "Health check: http://0.0.0.0:$PORT/health"
echo "=========================================="

# Use exec to replace shell process with uvicorn
# This ensures proper signal handling for Railway
exec uvicorn app.main:app --host 0.0.0.0 --port "$PORT"
