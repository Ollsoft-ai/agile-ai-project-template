import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.database import create_db_and_tables
from app.routers import upload, authors, auth
from app.supertokens_config import init_supertokens

# SuperTokens imports
from supertokens_python import get_all_cors_headers
from supertokens_python.framework.fastapi import get_middleware

# Only use /api root_path in production
root_path = "/api" if os.getenv("ENVIRONMENT") == "production" else ""

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handle application startup and shutdown"""
    # Startup
    create_db_and_tables()
    yield
    # Shutdown
    pass

app = FastAPI(
    title="Agile AI Backend",
    description="Modern FastAPI backend with SQLModel, PostgreSQL, and Alembic",
    version="0.1.0",
    root_path=root_path,
    lifespan=lifespan
)

# Initialize SuperTokens BEFORE adding middleware
init_supertokens()

# Add SuperTokens middleware FIRST (before CORS)
app.add_middleware(get_middleware())

# Configure CORS with SuperTokens headers
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Frontend URLs
    allow_credentials=True,
    allow_methods=["GET", "PUT", "POST", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=["Content-Type"] + get_all_cors_headers(),
)

# Include routers
app.include_router(upload.router, prefix="/upload", tags=["upload"])
app.include_router(authors.router, prefix="/authors", tags=["authors"])
app.include_router(auth.router, prefix="/auth", tags=["authentication"])

@app.get("/")
async def read_root():
    return {"message": "Agile AI Backend API", "version": "0.1.0"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "database": "connected"}