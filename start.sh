#!/bin/bash
set +e

export PYTHONUNBUFFERED=1

echo "SCRIPT STARTED" >&2
echo "SCRIPT STARTED"

PORT=${PORT:-8000}

echo "=========================================="
echo "Starting Course Registration API"
echo "Server will listen on port: $PORT"
echo "=========================================="

echo "Testing Python import..."
python -c "import sys; print('Python', sys.version)" || {
  echo "ERROR: Python import failed!"
  exit 1
}

# Start migrations in the background (NON-BLOCKING)
echo "Starting database migrations in background..."
(
  echo "[migrations] alembic upgrade head starting..."
  alembic upgrade head
  code=$?
  if [ $code -eq 0 ]; then
    echo "[migrations] ✓ completed successfully"
  else
    echo "[migrations] ⚠ failed with exit code $code (continuing anyway)"
  fi
) &

# Optional: quick import test (should be fast)
echo "Testing application import..."
python test_startup.py || {
  echo "WARNING: Failed to import application (continuing anyway)"
}

echo "Starting FastAPI server on 0.0.0.0:$PORT..."
echo "Health check: http://0.0.0.0:$PORT/health"
echo "=========================================="

# Start the server immediately
exec uvicorn app.main:app --host 0.0.0.0 --port "$PORT"
