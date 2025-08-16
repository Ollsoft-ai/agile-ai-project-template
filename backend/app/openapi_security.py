# app/openapi_security.py
from fastapi.security import OAuth2AuthorizationCodeBearer
from app.settings import settings

# For per-provider issuer, the endpoints are stable:
AUTHZ_URL = settings.AUTHENTIK_ISSUER.rstrip("/") + "/authorize"
TOKEN_URL = settings.AUTHENTIK_ISSUER.rstrip("/") + "/token"

oauth2_auth = OAuth2AuthorizationCodeBearer(
    authorizationUrl=AUTHZ_URL,
    tokenUrl=TOKEN_URL,
    scopes={
        "openid": "OpenID Connect",
        "email": "User email",
        "profile": "Basic profile",
        "groups": "User groups claim",
    },
)
