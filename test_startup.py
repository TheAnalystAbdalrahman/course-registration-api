#!/usr/bin/env python3
"""Test script to verify app can start"""
import sys

print("Testing imports...", file=sys.stderr)
print("Testing imports...")

try:
    print("Importing config...", file=sys.stderr)
    from app.config import settings
    print(f"Config loaded. DATABASE_URL present: {settings.database_url is not None}", file=sys.stderr)
    
    print("Importing database...", file=sys.stderr)
    from app.database import Base, get_db
    print("Database imported", file=sys.stderr)
    
    print("Importing main app...", file=sys.stderr)
    from app.main import app
    print("App imported successfully!", file=sys.stderr)
    print("SUCCESS: All imports passed")
    sys.exit(0)
except Exception as e:
    print(f"ERROR: {e}", file=sys.stderr)
    import traceback
    traceback.print_exc()
    sys.exit(1)

