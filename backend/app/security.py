import time
import httpx
from typing import Dict, Any
from fastapi import HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.settings import settings

# Use Authlib for robust JWT validation with JWK sets
from authlib.jose import jwt as authlib_jwt
from authlib.jose import JsonWebKey

_bearer = HTTPBearer(auto_error=True)

class _Cache:
    conf: Dict[str, Any] | None = None
    jwks: Dict[str, Any] | None = None
    ts_conf: float = 0.0
    ts_jwks: float = 0.0

_cache = _Cache()

async def _get_openid_conf() -> Dict[str, Any]:
    if not _cache.conf or time.time() - _cache.ts_conf > 300:
        async with httpx.AsyncClient(timeout=settings.HTTP_TIMEOUT) as c:
            r = await c.get(settings.AUTHENTIK_ISSUER.rstrip("/") + "/.well-known/openid-configuration")
            r.raise_for_status()
            _cache.conf = r.json()
            _cache.ts_conf = time.time()
    return _cache.conf

async def _get_jwks() -> Dict[str, Any]:
    conf = await _get_openid_conf()
    if not _cache.jwks or time.time() - _cache.ts_jwks > 300:
        async with httpx.AsyncClient(timeout=settings.HTTP_TIMEOUT) as c:
            r = await c.get(conf["jwks_uri"])
            r.raise_for_status()
            _cache.jwks = r.json()
            _cache.ts_jwks = time.time()
    return _cache.jwks

async def get_claims(creds: HTTPAuthorizationCredentials = Security(_bearer)) -> Dict[str, Any]:
    """Validate a Bearer JWT against the issuer's JWKS and return claims."""
    token = creds.credentials
    jwks = await _get_jwks()
    keyset = JsonWebKey.import_key_set(jwks)
    # Validate iss and aud; exp/nbf/iat are validated by .validate()
    claims = authlib_jwt.decode(
        token,
        keyset,
        claims_options={
            "iss": {"values": [settings.AUTHENTIK_ISSUER.rstrip('/') + '/']},
            "aud": {"values": [settings.OIDC_CLIENT_ID]},
        },
    )
    try:
        claims.validate()  # raises if expired/invalid
    except Exception as e:  # Authlib’s specific errors derive from Exception
        raise HTTPException(status_code=401, detail=f"Invalid token: {e}")
    return dict(claims)

async def get_claims_from_token(token: str) -> dict:
    jwks = await _get_jwks()
    keyset = JsonWebKey.import_key_set(jwks)
    claims = authlib_jwt.decode(
        token,
        keyset,
        claims_options={
            "iss": {"values": [settings.AUTHENTIK_ISSUER.rstrip('/') + '/']},
            "aud": {"values": [settings.OIDC_CLIENT_ID]},
        },
    )
    claims.validate()
    return dict(claims)