"""
Dependency injection functions for the FastAPI application.
"""

from typing import Annotated
from fastapi import Header, HTTPException


async def get_token_header(x_token: Annotated[str, Header()] = None):
    """
    Dependency for token-based authentication.
    This is a placeholder - implement proper authentication in production.
    """
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")


async def get_query_token(token: str = None):
    """
    Dependency for query parameter token authentication.
    This is a placeholder - implement proper authentication in production.
    """
    if token != "jessica":
        raise HTTPException(status_code=400, detail="No Jessica token provided")