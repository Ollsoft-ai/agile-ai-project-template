import os
from sqlmodel import SQLModel, create_engine, Session
from typing import Generator

# Database URL configuration
DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql://ollsoft:0lls0ft231!@localhost:5432/app_db"
)

# Create engine with appropriate settings
def get_engine(database_url: str = None):
    """Create database engine with proper configuration"""
    url = database_url or DATABASE_URL
    
    # Engine configuration
    engine_kwargs = {
        "echo": os.getenv("ENVIRONMENT") == "development",  # SQL logging in dev
        "pool_pre_ping": True,  # Verify connections before use
        "pool_recycle": 300,    # Recycle connections every 5 minutes
    }
    
    return create_engine(url, **engine_kwargs)

# Default engine
engine = get_engine()

def create_db_and_tables():
    """Create all database tables"""
    SQLModel.metadata.create_all(engine)

def get_session() -> Generator[Session, None, None]:
    """Dependency to get database session"""
    with Session(engine) as session:
        yield session
