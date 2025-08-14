# SuperTokens Backend Integration

This document explains the SuperTokens integration in your FastAPI backend.

## 🏗️ **Architecture Overview**

```
Frontend (Svelte) ←→ Backend (FastAPI) ←→ SuperTokens Core ←→ PostgreSQL
```

- **Frontend**: Makes auth requests to `/api/auth/*`
- **Backend**: Handles auth via SuperTokens Python SDK
- **SuperTokens Core**: Manages sessions and auth logic
- **PostgreSQL**: Stores user data and sessions

## 📁 **Files Added/Modified**

| File | Purpose |
|------|---------|
| `app/supertokens_config.py` | SuperTokens initialization and configuration |
| `app/routers/auth.py` | Protected routes and auth endpoints |
| `app/main.py` | Updated with SuperTokens middleware |
| `requirements.txt` | Added `supertokens-python==0.30.2` |
| `docker-compose.yml` | Added SuperTokens Core service |

## 🔧 **Configuration**

### Environment Variables

```bash
# Development (defaults)
SUPERTOKENS_CONNECTION_URI=http://supertokens:3567

# Production (recommended)
SUPERTOKENS_CONNECTION_URI=http://your-supertokens-core:3567
SUPERTOKENS_API_KEY=your-api-key-here
```

### Request Flow

**Development:**
- Frontend: `http://localhost:3000/api/auth/signin`
- Vite Proxy: Forwards to `http://backend:8000/auth/signin`
- Backend: Handles via SuperTokens middleware

**Production:**
- Frontend: `http://your-domain/api/auth/signin`
- Nginx: Forwards to backend
- Backend: Handles auth at `/api/auth/*`

## 🛡️ **Protected Routes**

### Using Session Verification

```python
from supertokens_python.recipe.session.framework.fastapi import verify_session
from supertokens_python.recipe.session import SessionContainer
from fastapi import Depends

@app.get("/protected")
async def protected_route(session: SessionContainer = Depends(verify_session())):
    user_id = session.get_user_id()
    return {"user_id": user_id, "message": "Access granted"}
```

### Available Protected Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/auth/user/profile` | GET | Get user profile |
| `/auth/user/update-metadata` | POST | Update user data |
| `/auth/dashboard/stats` | GET | Dashboard statistics |
| `/auth/admin/users` | GET | Admin-only endpoint |

## 🐳 **Docker Setup**

The Docker configuration includes:

1. **SuperTokens Core**: `registry.supertokens.io/supertokens/supertokens-postgresql:latest`
2. **PostgreSQL**: Shared database for app data and SuperTokens
3. **Backend**: FastAPI with SuperTokens Python SDK

### Starting Services

```bash
# Development
docker-compose up --build

# Production
docker-compose -f docker-compose.prod.yml up --build
```

## 🔍 **Testing Authentication**

### 1. **Check SuperTokens Core**
```bash
curl http://localhost:3567/hello
# Should return: Hello
```

### 2. **Test Sign Up** (via frontend)
- Navigate to `http://localhost:3000/auth`
- Create account with email/password
- Check browser network tab for auth requests

### 3. **Test Protected Route**
```bash
# After signing in via frontend
curl -X GET http://localhost:8000/auth/user/profile \
  -H "Cookie: sAccessToken=..." \
  -H "Content-Type: application/json"
```

## 🚨 **Troubleshooting**

### Common Issues

**1. CORS Errors**
- Ensure frontend URL is in `allow_origins` list
- Check SuperTokens headers are included in CORS config

**2. SuperTokens Core Connection**
- Verify `SUPERTOKENS_CONNECTION_URI` environment variable
- Check SuperTokens Core service is running (`docker-compose ps`)

**3. Session Issues**
- Clear browser cookies
- Check cookie domain settings in `supertokens_config.py`

### Debug Mode

Set environment variable to enable debug logging:
```bash
export ENVIRONMENT=development
```

## 📚 **References**

- [SuperTokens Python SDK](https://supertokens.com/docs/quickstart/backend-setup)
- [FastAPI Integration](https://supertokens.com/docs/community/guides/fasapi-integration)
- [Session Management](https://supertokens.com/docs/additional-verification/session-verification/protect-api-routes)
- [Self-hosting SuperTokens](https://supertokens.com/docs/deployment/self-host-supertokens)

## 🔐 **Production Considerations**

1. **Use your own SuperTokens Core instance** (not `try.supertokens.com`)
2. **Set strong API keys** for SuperTokens Core
3. **Configure proper CORS origins** (no wildcards)
4. **Enable HTTPS** for production deployments
5. **Set up monitoring** for SuperTokens Core health
