#!/usr/bin/env python3
"""
Railway entrypoint script - runs migrations and starts the server
"""
import os
import sys
import subprocess

# Ensure unbuffered output
os.environ["PYTHONUNBUFFERED"] = "1"

print("=" * 50, flush=True)
print("Starting Course Registration API", flush=True)
print("=" * 50, flush=True)

# Get port from environment
port = os.environ.get("PORT", "8000")
print(f"Server will listen on port: {port}", flush=True)

# Run migrations (non-blocking)
print("Running database migrations...", flush=True)
migration_result = subprocess.run(
    ["alembic", "upgrade", "head"],
    capture_output=True,
    text=True
)
if migration_result.returncode == 0:
    print("✓ Database migrations completed successfully", flush=True)
else:
    print("⚠ WARNING: Database migrations failed, but continuing startup...", flush=True)
    print(migration_result.stderr, flush=True)
    print("  The application will start, but database operations may fail.", flush=True)

# Start the server
print("Starting FastAPI server...", flush=True)
print(f"Health check: http://0.0.0.0:{port}/health", flush=True)
print("=" * 50, flush=True)

# Start uvicorn - this replaces the Python process
os.execvp(
    "uvicorn",
    [
        "uvicorn",
        "app.main:app",
        "--host", "0.0.0.0",
        "--port", port
    ]
)

