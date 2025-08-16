from fastapi import APIRouter, Depends
from app.security import get_claims
from app.guards import require_groups, require_scopes, require_claim_equals, is_authenticated

router = APIRouter(prefix="", tags=["api"])

@router.get("/ping")
async def ping():
    return {"pong": True}

@router.get("/dashboard")
async def dashboard(user = Depends(is_authenticated)):
    return {"hello": user.get("email") or user.get("sub")}

@router.get("/profile")
async def profile(claims = Depends(get_claims)):
    # user is authenticated if we got here; `claims` are the JWT claims
    return {"sub": claims["sub"], "email": claims.get("email")}

@router.get("/admin")
async def admin_only(_=Depends(require_groups("admins"))):
    return {"ok": True, "who": "admins only"}

@router.get("/ops-any")
async def ops_any(_=Depends(require_groups("devops", "platform", any_match=True))):
    return {"ok": True, "who": "devops OR platform"}

@router.get("/reports")
async def reports_read(_=Depends(require_scopes("reports:read"))):
    return {"ok": True}

@router.post("/billing/run")
async def billing_run(_=Depends(require_scopes("billing:run", "reports:write"))):
    return {"ok": True}

@router.get("/super")
async def super_claim(_=Depends(require_claim_equals("role", "superuser"))):
    return {"ok": True}
