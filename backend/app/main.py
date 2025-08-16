import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from starlette.middleware.sessions import SessionMiddleware

from app.database import create_db_and_tables
from app.routers import upload, authors, authentication_testing, auth_routes
from app.settings import settings

# Only use /api root_path in production
root_path = "/api" if settings.ENVIRONMENT == "production" else ""

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handle application startup and shutdown"""
    # Startup
    create_db_and_tables()
    yield
    # Shutdown
    pass

swagger_ui_init_oauth = {
    "clientId": "fastapi-swagger-oidc",
    "usePkceWithAuthorizationCode": True,
    "scopes": "openid email profile groups",
}

app = FastAPI(
    title="Agile AI Backend",
    description="Modern FastAPI backend with SQLModel, PostgreSQL, and Alembic",
    version="0.1.0",
    root_path=root_path,
    lifespan=lifespan,
    swagger_ui_init_oauth=swagger_ui_init_oauth
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(SessionMiddleware, secret_key=settings.SESSION_SECRET)

# Include routers
app.include_router(upload.router, prefix="/upload", tags=["upload"])
app.include_router(authors.router, prefix="/authors", tags=["authors"])
app.include_router(authentication_testing.router, tags=["api"])
app.include_router(auth_routes.router, tags=["auth"])

@app.get("/")
async def read_root():
    return {"message": "Agile AI Backend API", "version": "0.1.0"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "database": "connected"}