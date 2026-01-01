#!/bin/bash
set -e

echo "=========================================="
echo "Starting Course Registration API"
echo "=========================================="

# Check if DATABASE_URL is set
if [ -z "$DATABASE_URL" ]; then
    echo "ERROR: DATABASE_URL environment variable is not set!"
    echo "Please configure DATABASE_URL in Railway project settings."
    exit 1
fi

echo "DATABASE_URL is set (length: ${#DATABASE_URL} characters)"

# Run migrations with error handling
echo "Running database migrations..."
if ! alembic upgrade head; then
    echo "ERROR: Database migrations failed!"
    echo "This might be due to:"
    echo "  1. Invalid DATABASE_URL"
    echo "  2. Database not accessible"
    echo "  3. Network connectivity issues"
    exit 1
fi

echo "Migrations completed successfully!"

# Start the server
echo "Starting FastAPI server on port ${PORT:-8000}..."
exec uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}

