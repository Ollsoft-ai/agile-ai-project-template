from typing import Callable
from fastapi import Depends, HTTPException, status
from app.security import get_claims

def is_authenticated(claims=Depends(get_claims)):
    if not claims:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return claims

def require_groups(*needed: str, any_match: bool = False) -> Callable:
    """
    Ensure the token contains a 'groups' claim with required group(s).
    'groups' is expected to be a list of names coming from an Authentik scope mapping.
    """
    async def dep(claims=Depends(get_claims)):
        groups = set(claims.get("groups") or [])
        ok = bool(groups.intersection(needed)) if any_match else set(needed).issubset(groups)
        if not ok:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient group")
        return claims
    return dep

def require_scopes(*needed: str, any_match: bool = False) -> Callable:
    """
    Check OAuth scopes from the 'scope' claim (space-separated string).
    """
    async def dep(claims=Depends(get_claims)):
        token_scopes = set((claims.get("scope") or "").split())
        ok = bool(token_scopes.intersection(needed)) if any_match else set(needed).issubset(token_scopes)
        if not ok:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient scope")
        return claims
    return dep

def require_claim_equals(claim: str, *expected) -> Callable:
    """
    Generic checker for any claim. If the claim is a list, verifies all expected are present.
    """
    async def dep(claims=Depends(get_claims)):
        value = claims.get(claim)
        if isinstance(value, list):
            ok = set(expected).issubset(set(value))
        else:
            ok = value in expected
        if not ok:
            raise HTTPException(status_code=403, detail=f"Missing/invalid claim: {claim}")
        return claims
    return dep
