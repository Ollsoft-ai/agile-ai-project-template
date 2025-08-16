from pydantic import BaseModel
import os

class Settings(BaseModel):
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    
    # Database URL
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://ollsoft:rOwFLeyVeAteLardstuRsFuLARyPEnte@postgres:5432/app_db")

    # Authentik issuer for this application (per-provider issuer recommended)
    AUTHENTIK_ISSUER: str = os.getenv("AUTHENTIK_ISSUER", "http://localhost:9000/application/o/fastapi-demo/")
    OIDC_CLIENT_ID: str = os.getenv("OIDC_CLIENT_ID", "fastapi-client")
    OIDC_CLIENT_SECRET: str = os.getenv("OIDC_CLIENT_SECRET", "change-me-very-long-random")

    # Your app base URL (used for redirect URI in the web flow)
    APP_BASE_URL: str = os.getenv("APP_BASE_URL", "http://localhost:8000")

    # Session secret for Starlette sessions (browser flow)
    SESSION_SECRET: str = os.getenv("SESSION_SECRET", "replace-with-long-random")

    # HTTP timeouts (s)
    HTTP_TIMEOUT: float = float(os.getenv("HTTP_TIMEOUT", "10"))

settings = Settings()
