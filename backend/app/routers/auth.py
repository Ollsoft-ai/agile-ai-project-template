"""
Authentication routes and protected endpoints
"""
from fastapi import APIRouter, Depends, HTTPException
from supertokens_python.recipe.session.framework.fastapi import verify_session
from supertokens_python.recipe.session import SessionContainer
from typing import Dict, Any

router = APIRouter()

@router.get("/user/profile")
async def get_user_profile(session: SessionContainer = Depends(verify_session())):
    """
    Protected route - Get current user's profile
    Requires valid session
    """
    user_id = session.get_user_id()
    user_metadata = session.get_access_token_payload()
    
    return {
        "user_id": user_id,
        "metadata": user_metadata,
        "message": "Successfully retrieved user profile"
    }

@router.post("/user/update-metadata")
async def update_user_metadata(
    metadata: Dict[str, Any],
    session: SessionContainer = Depends(verify_session())
):
    """
    Protected route - Update user metadata
    Requires valid session
    """
    user_id = session.get_user_id()
    
    # In a real app, you would update user data in your database here
    # For demo purposes, we'll just return the data
    
    return {
        "user_id": user_id,
        "updated_metadata": metadata,
        "message": "User metadata updated successfully"
    }

@router.get("/dashboard/stats")
async def get_dashboard_stats(session: SessionContainer = Depends(verify_session())):
    """
    Protected route - Get dashboard statistics
    Requires valid session
    """
    user_id = session.get_user_id()
    
    # Mock dashboard data
    return {
        "user_id": user_id,
        "stats": {
            "total_uploads": 42,
            "documents_processed": 38,
            "last_login": "2024-01-15T10:30:00Z"
        },
        "message": "Dashboard stats retrieved successfully"
    }

@router.post("/protected-action")
async def protected_action(
    data: Dict[str, Any],
    session: SessionContainer = Depends(verify_session())
):
    """
    Example protected route that requires authentication
    """
    user_id = session.get_user_id()
    
    return {
        "user_id": user_id,
        "action": "completed",
        "data_received": data,
        "message": f"Protected action completed for user {user_id}"
    }

# Optional: Route with custom session verification
@router.get("/admin/users")
async def get_all_users(session: SessionContainer = Depends(verify_session())):
    """
    Admin-only route (you would add role checking here)
    """
    user_id = session.get_user_id()
    user_metadata = session.get_access_token_payload()
    
    # In a real app, you would check user roles here
    # For now, just return demo data
    
    return {
        "admin_user_id": user_id,
        "users": [
            {"id": "user1", "email": "user1@example.com"},
            {"id": "user2", "email": "user2@example.com"}
        ],
        "message": "Admin access granted"
    }
