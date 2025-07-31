from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import upload

app = FastAPI(
    title="ClearPath Trade AI Platform",
    description="AI-powered trade compliance platform",
    version="0.1.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(upload.router)

@app.get("/")
async def read_root():
    return {"message": "ClearPath Trade AI Platform API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}