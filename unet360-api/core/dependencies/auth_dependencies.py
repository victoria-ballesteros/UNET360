from fastapi import Request, HTTPException, Depends, status

async def get_current_admin_user(request: Request):
    user_id = request.state.user_id
    user_role = request.state.user_role

    if not user_id or not user_role:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required. User information not found in request state."
        )

    if user_role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied. Only administrators can perform this operation."
        )
    
    return user_id