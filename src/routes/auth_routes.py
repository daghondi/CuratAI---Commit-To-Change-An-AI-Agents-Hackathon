"""
FastAPI authentication and authorization endpoints.
Provides login, registration, token refresh, and permission checking.
"""

from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, EmailStr, validator
from typing import Optional
from datetime import datetime

from auth import (
    get_auth_service,
    AuthenticationService,
    SubscriptionTier,
    PermissionManager,
    UserRole,
)

router = APIRouter(prefix="/api/auth", tags=["authentication"])


# Request/Response models
class RegisterRequest(BaseModel):
    """User registration request"""
    email: EmailStr
    password: str
    artist_name: str
    
    @validator('password')
    def password_strength(cls, v):
        """Validate password strength"""
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters')
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain at least one digit')
        return v
    
    @validator('artist_name')
    def artist_name_length(cls, v):
        """Validate artist name"""
        if not v or len(v.strip()) == 0:
            raise ValueError('Artist name is required')
        if len(v) > 100:
            raise ValueError('Artist name must be less than 100 characters')
        return v.strip()


class LoginRequest(BaseModel):
    """User login request"""
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    """Authentication token response"""
    access_token: str
    refresh_token: Optional[str] = None
    token_type: str = "bearer"
    expires_in: int = 3600
    user: dict


class UserResponse(BaseModel):
    """User account response"""
    user_id: str
    email: str
    artist_name: str
    role: str
    subscription_tier: str
    verified: bool
    avatar_url: Optional[str] = None
    bio: Optional[str] = None
    created_at: datetime
    last_login: Optional[datetime] = None


class VerifyTokenRequest(BaseModel):
    """Token verification request"""
    token: str


class RefreshTokenRequest(BaseModel):
    """Refresh token request"""
    refresh_token: str


class LogoutRequest(BaseModel):
    """Logout request"""
    refresh_token: str


class PasswordResetRequest(BaseModel):
    """Password reset request"""
    email: EmailStr


class PasswordResetConfirm(BaseModel):
    """Password reset confirmation"""
    email: EmailStr
    reset_token: str
    new_password: str


class UpgradeSubscriptionRequest(BaseModel):
    """Subscription upgrade request"""
    tier: str


# Helper functions
async def get_current_user(token: str = None) -> dict:
    """
    Get current user from token.
    Can be used as a dependency in route handlers.
    """
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    auth = get_auth_service()
    try:
        payload = auth.verify_token(token)
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
        return {"user_id": user_id, "email": payload.get("email")}
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
        )


# Authentication endpoints
@router.post("/register", response_model=TokenResponse, status_code=201)
async def register(request: RegisterRequest):
    """
    Register a new user account.
    
    **Request:**
    - email: Valid email address
    - password: Minimum 8 chars, 1 uppercase, 1 digit
    - artist_name: Display name for artist profile
    
    **Response:**
    - access_token: JWT for API requests
    - refresh_token: Token for refreshing access
    - user: User account details
    
    **Errors:**
    - 400: Invalid input or email already registered
    - 409: Email conflict
    """
    auth = get_auth_service()
    
    try:
        # Register user
        user = auth.register(
            email=request.email,
            password=request.password,
            artist_name=request.artist_name
        )
        
        # Auto-login after registration
        token = auth.login(request.email, request.password)
        
        return TokenResponse(
            access_token=token.access_token,
            refresh_token=token.refresh_token,
            user={
                "user_id": user.user_id,
                "email": user.email,
                "artist_name": user.artist_name,
                "role": user.role.value,
                "subscription_tier": user.subscription_tier.value,
                "verified": user.verified,
            }
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/login", response_model=TokenResponse)
async def login(request: LoginRequest):
    """
    Authenticate user with email and password.
    
    **Request:**
    - email: Registered email address
    - password: Account password
    
    **Response:**
    - access_token: JWT for API requests
    - refresh_token: Token for refreshing access
    - user: User account details
    
    **Errors:**
    - 401: Invalid credentials
    - 403: Account locked (too many failed attempts)
    """
    auth = get_auth_service()
    
    try:
        token = auth.login(request.email, request.password)
        user = auth.get_user(token.user_id)
        
        return TokenResponse(
            access_token=token.access_token,
            refresh_token=token.refresh_token,
            expires_in=token.expires_in,
            user={
                "user_id": user.user_id,
                "email": user.email,
                "artist_name": user.artist_name,
                "role": user.role.value,
                "subscription_tier": user.subscription_tier.value,
                "verified": user.verified,
            }
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e)
        )


@router.post("/logout", status_code=204)
async def logout(request: LogoutRequest):
    """
    Logout user by invalidating refresh token.
    
    **Request:**
    - refresh_token: Token to invalidate
    """
    auth = get_auth_service()
    auth.logout(request.refresh_token)
    return None


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(request: RefreshTokenRequest):
    """
    Refresh access token using refresh token.
    
    **Request:**
    - refresh_token: Valid refresh token from login
    
    **Response:**
    - access_token: New JWT for API requests
    
    **Errors:**
    - 401: Invalid or expired refresh token
    """
    auth = get_auth_service()
    
    try:
        token = auth.refresh_access_token(request.refresh_token)
        user = auth.get_user(token.user_id)
        
        return TokenResponse(
            access_token=token.access_token,
            refresh_token=request.refresh_token,
            expires_in=token.expires_in,
            user={
                "user_id": user.user_id,
                "email": user.email,
                "artist_name": user.artist_name,
                "role": user.role.value,
                "subscription_tier": user.subscription_tier.value,
                "verified": user.verified,
            }
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e)
        )


@router.get("/me", response_model=UserResponse)
async def get_current_user_endpoint(token: str = None):
    """
    Get current authenticated user.
    
    **Headers:**
    - Authorization: Bearer {access_token}
    
    **Response:**
    - User account details
    
    **Errors:**
    - 401: Invalid or missing token
    """
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
        )
    
    auth = get_auth_service()
    
    try:
        payload = auth.verify_token(token)
        user_id = payload.get("sub")
        user = auth.get_user(user_id)
        
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        
        return UserResponse(
            user_id=user.user_id,
            email=user.email,
            artist_name=user.artist_name,
            role=user.role.value,
            subscription_tier=user.subscription_tier.value,
            verified=user.verified,
            avatar_url=user.avatar_url,
            bio=user.bio,
            created_at=user.created_at,
            last_login=user.last_login,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e)
        )


@router.post("/verify-token", status_code=200)
async def verify_token(request: VerifyTokenRequest):
    """
    Verify JWT token validity.
    
    **Request:**
    - token: JWT token to verify
    
    **Response:**
    - valid: Boolean indicating if token is valid
    - payload: Decoded token data
    
    **Errors:**
    - 401: Invalid or expired token
    """
    auth = get_auth_service()
    
    try:
        payload = auth.verify_token(request.token)
        return {
            "valid": True,
            "payload": payload
        }
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e)
        )


@router.post("/password-reset/request")
async def request_password_reset(request: PasswordResetRequest):
    """
    Request password reset token via email.
    
    **Request:**
    - email: User email address
    
    **Response:**
    - message: Confirmation message
    
    **Note:** In production, send reset token via email
    """
    auth = get_auth_service()
    
    try:
        reset_token = auth.request_password_reset(request.email)
        
        # In production, send email with reset link
        # For demo, return token (not recommended in production)
        return {
            "message": "Password reset token generated",
            "reset_token": reset_token  # Remove in production
        }
    except ValueError:
        # Don't reveal if email exists
        return {
            "message": "If email exists, reset token has been sent"
        }


@router.post("/password-reset/confirm")
async def confirm_password_reset(request: PasswordResetConfirm):
    """
    Confirm password reset with token.
    
    **Request:**
    - email: User email address
    - reset_token: Token from password reset email
    - new_password: New password (must meet strength requirements)
    
    **Response:**
    - message: Confirmation message
    
    **Errors:**
    - 400: Invalid reset token or requirements not met
    """
    auth = get_auth_service()
    
    try:
        user = auth.reset_password(
            email=request.email,
            reset_token=request.reset_token,
            new_password=request.new_password
        )
        
        return {
            "message": "Password reset successful",
            "user_id": user.user_id
        }
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/email/verify")
async def verify_email(user_id: str, token: str):
    """
    Verify email address with token.
    
    **Query Parameters:**
    - user_id: User ID
    - token: Verification token from email
    
    **Response:**
    - message: Verification status
    
    **Errors:**
    - 400: Invalid token
    """
    auth = get_auth_service()
    
    try:
        user = auth.verify_email(user_id, token)
        return {
            "message": "Email verified successfully",
            "user_id": user.user_id
        }
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/subscription/upgrade")
async def upgrade_subscription(
    request: UpgradeSubscriptionRequest,
    token: str = None
):
    """
    Upgrade user subscription tier.
    
    **Headers:**
    - Authorization: Bearer {access_token}
    
    **Request:**
    - tier: 'pro' or 'enterprise'
    
    **Response:**
    - message: Upgrade confirmation
    - subscription_tier: New tier
    
    **Errors:**
    - 401: Not authenticated
    - 400: Invalid tier
    """
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
        )
    
    auth = get_auth_service()
    
    try:
        payload = auth.verify_token(token)
        user_id = payload.get("sub")
        
        # Validate tier
        try:
            tier = SubscriptionTier(request.tier.lower())
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid tier: {request.tier}"
            )
        
        user = auth.upgrade_subscription(user_id, tier)
        
        return {
            "message": f"Upgraded to {tier.value}",
            "subscription_tier": user.subscription_tier.value,
            "features": PermissionManager.TIER_FEATURES.get(tier, {})
        }
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e)
        )


# Health check
@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "authentication"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(router, host="0.0.0.0", port=8000)
