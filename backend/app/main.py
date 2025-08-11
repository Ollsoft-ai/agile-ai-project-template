import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import upload

# Only use /api root_path in production
root_path = "/api" if os.getenv("ENVIRONMENT") == "production" else ""

app = FastAPI(
    title="Ollsoft Backend",
    description="Ollsoft Backend",
    version="0.1.0",
    root_path=root_path
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(upload.router)

@app.get("/")
async def read_root():
    return {"message": "Ollsoft Backend API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}