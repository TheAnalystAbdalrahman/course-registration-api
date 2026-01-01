"""
Custom exception helpers for HTTP error responses
"""
from fastapi import HTTPException


def not_found(resource: str, id: int) -> HTTPException:
    """Return a 404 Not Found exception."""
    return HTTPException(status_code=404, detail=f"{resource} with id {id} not found")


def conflict(message: str) -> HTTPException:
    """Return a 409 Conflict exception."""
    return HTTPException(status_code=409, detail=message)


def bad_request(message: str) -> HTTPException:
    """Return a 400 Bad Request exception."""
    return HTTPException(status_code=400, detail=message)

