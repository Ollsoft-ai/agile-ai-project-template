from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import RedirectResponse, JSONResponse
from authlib.integrations.starlette_client import OAuth, OAuthError
from app.settings import settings

router = APIRouter(prefix="", tags=["auth"])

oauth = OAuth()
oauth.register(
    name="authentik",
    server_metadata_url=settings.AUTHENTIK_ISSUER.rstrip("/") + "/.well-known/openid-configuration",
    client_id=settings.OIDC_CLIENT_ID,
    client_secret=settings.OIDC_CLIENT_SECRET,
    client_kwargs={"scope": "openid email profile offline_access groups"},
)

@router.get("/login")
async def login(request: Request):
    redirect_uri = settings.APP_BASE_URL.rstrip("/") + "/auth/callback"
    return await oauth.authentik.authorize_redirect(request, redirect_uri)

@router.get("/auth/callback")
async def auth_callback(request: Request):
    try:
        token = await oauth.authentik.authorize_access_token(request)
        id_claims = await oauth.authentik.parse_id_token(request, token)
        # persist minimal user info + raw token in the session for browser usage
        request.session["user"] = {
            "sub": id_claims.get("sub"),
            "email": id_claims.get("email"),
            "name": id_claims.get("name"),
        }
        request.session["token"] = token
        return RedirectResponse(url="/me")
    except OAuthError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/me")
async def me(request: Request):
    user = request.session.get("user")
    if not user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return JSONResponse(user)

@router.post("/logout")
async def logout(request: Request):
    request.session.clear()
    return {"ok": True}
