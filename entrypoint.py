#!/usr/bin/env python3
import os
import sys
import subprocess

os.environ["PYTHONUNBUFFERED"] = "1"

print("=" * 50, flush=True)
print("Starting Course Registration API", flush=True)
print("=" * 50, flush=True)

port = os.environ.get("PORT", "8000")
print(f"Server will listen on port: {port}", flush=True)

print("Starting database migrations in background...", flush=True)
try:
    subprocess.Popen(
        ["alembic", "upgrade", "head"],
        stdout=sys.stdout,
        stderr=sys.stderr,
        text=True,
    )
except Exception as e:
    print(f"⚠ WARNING: Failed to start migrations: {e}", flush=True)

print("Starting FastAPI server immediately...", flush=True)
print(f"Health check: http://0.0.0.0:{port}/health", flush=True)
print("=" * 50, flush=True)

os.execvp(
    "uvicorn",
    ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", port]
)
