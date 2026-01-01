#!/bin/bash
# Don't exit on error - we want the server to start even if migrations fail
set +e

echo "=========================================="
echo "Starting Course Registration API"
echo "=========================================="

# Get port from environment or default to 8000
PORT=${PORT:-8000}
echo "Server will listen on port: $PORT"

# Run migrations in background (non-blocking)
# If migrations fail, log the error but continue
echo "Running database migrations (non-blocking)..."
if alembic upgrade head 2>&1; then
    echo "✓ Database migrations completed successfully"
else
    echo "⚠ WARNING: Database migrations failed, but continuing startup..."
    echo "  The application will start, but database operations may fail."
    echo "  Run migrations manually when the database is available."
fi

# Start the server
echo "Starting FastAPI server on 0.0.0.0:$PORT..."
echo "Health check available at: http://0.0.0.0:$PORT/health"
echo "=========================================="

# Use exec to replace shell process with uvicorn
exec uvicorn app.main:app --host 0.0.0.0 --port "$PORT"
