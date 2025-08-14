"""
SuperTokens configuration for FastAPI backend
"""
import os
import time
import requests
from supertokens_python import init, InputAppInfo, SupertokensConfig
from supertokens_python.recipe import emailpassword, session, dashboard

def wait_for_supertokens_core(connection_uri: str, max_retries: int = 30, delay: int = 1):
    """Wait for SuperTokens Core to be ready"""
    if not connection_uri or connection_uri.startswith("https://try.supertokens.com"):
        # Skip waiting for hosted service
        return
    
    print(f"Waiting for SuperTokens Core at {connection_uri}...")
    
    for attempt in range(max_retries):
        try:
            response = requests.get(f"{connection_uri}/hello", timeout=5)
            if response.status_code == 200:
                print(f"SuperTokens Core is ready! (attempt {attempt + 1})")
                return
        except requests.exceptions.RequestException:
            pass
        
        print(f"SuperTokens Core not ready, retrying in {delay}s... (attempt {attempt + 1}/{max_retries})")
        time.sleep(delay)
    
    print("Warning: SuperTokens Core may not be ready, proceeding anyway...")

def init_supertokens():
    """Initialize SuperTokens with configuration"""
    
    # Get environment-specific configuration
    environment = os.getenv("ENVIRONMENT", "development")
    connection_uri = os.getenv("SUPERTOKENS_CONNECTION_URI", "https://try.supertokens.com")
    
    # Wait for SuperTokens Core to be ready in Docker environment
    if connection_uri and not connection_uri.startswith("https://try.supertokens.com"):
        wait_for_supertokens_core(connection_uri)
    
    if environment == "production":
        # Production configuration - nginx routes everything
        api_domain = "http://localhost:3000"  # nginx proxy
        website_domain = "http://localhost:3000"
        api_base_path = "/api/auth"
        website_base_path = "/auth"
    else:
        # Development configuration  
        api_domain = "http://localhost:8000"  # direct backend access
        website_domain = "http://localhost:3000"  # frontend dev server
        api_base_path = "/auth"  # backend routes (after vite proxy strips /api)
        website_base_path = "/auth"
    
    init(
        app_info=InputAppInfo(
            app_name="Ollsoft",
            api_domain=api_domain,
            website_domain=website_domain,
            api_base_path=api_base_path,
            website_base_path=website_base_path
        ),
        supertokens_config=SupertokensConfig(
            # Use local SuperTokens Core from Docker Compose
            # Falls back to hosted version if not set
            connection_uri=connection_uri,
            api_key=os.getenv("SUPERTOKENS_API_KEY"),  # Optional
        ),
        framework='fastapi',
        recipe_list=[
            session.init(
                cookie_domain=None,  # Will be set based on request
                cookie_secure=environment == "production",
                cookie_same_site="lax"
            ),
            emailpassword.init(),
            dashboard.init()  # Enables the SuperTokens Dashboard UI
        ],
        mode='asgi'
    )
