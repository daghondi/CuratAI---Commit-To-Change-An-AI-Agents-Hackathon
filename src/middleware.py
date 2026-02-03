"""
FastAPI middleware for authentication and authorization.
Handles JWT token extraction, validation, and permission checking.
"""

from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse
from typing import Callable, Optional
import re

from auth import get_auth_service, PermissionManager, UserRole


class AuthenticationMiddleware:
    """Middleware to extract and validate JWT tokens from requests"""
    
    def __init__(self, app):
        self.app = app
    
    async def __call__(self, request: Request, call_next):
        """Process request and extract token"""
        # Extract token from Authorization header
        auth_header = request.headers.get("Authorization")
        token = None
        
        if auth_header:
            try:
                scheme, credentials = auth_header.split()
                if scheme.lower() == "bearer":
                    token = credentials
            except ValueError:
                pass
        
        # Store token in request state for use in route handlers
        request.state.token = token
        
        # Try to validate token and store user info
        if token:
            try:
                auth = get_auth_service()
                payload = auth.verify_token(token)
                request.state.user_id = payload.get("sub")
                request.state.email = payload.get("email")
                request.state.authenticated = True
            except Exception:
                request.state.authenticated = False
        else:
            request.state.authenticated = False
        
        response = await call_next(request)
        return response


class AuthorizationMiddleware:
    """Middleware to check user permissions for protected routes"""
    
    # Define protected routes and required permissions
    PROTECTED_ROUTES = {
        r"/api/opportunities/scout": ["opportunities:write"],
        r"/api/opportunities/\d+/delete": ["opportunities:delete"],
        r"/api/proposals": ["proposals:create"],
        r"/api/proposals/\d+/submit": ["proposals:submit"],
        r"/api/users": ["users:read"],
        r"/api/admin/": ["admin:*"],
    }
    
    def __init__(self, app):
        self.app = app
    
    async def __call__(self, request: Request, call_next):
        """Check authorization for protected routes"""
        # Check if route requires authorization
        path = request.url.path
        required_permissions = self._get_required_permissions(path)
        
        if required_permissions:
            # Check authentication
            if not getattr(request.state, "authenticated", False):
                return JSONResponse(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    content={"detail": "Authentication required"}
                )
            
            # Check permissions
            auth = get_auth_service()
            user_id = getattr(request.state, "user_id", None)
            user = auth.get_user(user_id)
            
            if not user:
                return JSONResponse(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    content={"detail": "User not found"}
                )
            
            # Check if user has required permissions
            has_permission = False
            for permission in required_permissions:
                if PermissionManager.has_permission(user, permission):
                    has_permission = True
                    break
            
            if not has_permission:
                return JSONResponse(
                    status_code=status.HTTP_403_FORBIDDEN,
                    content={
                        "detail": "Insufficient permissions",
                        "required": required_permissions
                    }
                )
        
        response = await call_next(request)
        return response
    
    def _get_required_permissions(self, path: str) -> Optional[list]:
        """Get required permissions for a route"""
        for pattern, permissions in self.PROTECTED_ROUTES.items():
            if re.match(pattern, path):
                return permissions
        return None


class RateLimitMiddleware:
    """Middleware to rate limit API requests"""
    
    def __init__(self, app, requests_per_minute: int = 60):
        self.app = app
        self.requests_per_minute = requests_per_minute
        self.request_history = {}
    
    async def __call__(self, request: Request, call_next):
        """Rate limit requests"""
        # Get client IP or user ID
        client_id = getattr(request.state, "user_id", None)
        if not client_id:
            client_id = request.client.host if request.client else "unknown"
        
        # Check rate limit
        import time
        current_time = time.time()
        
        if client_id not in self.request_history:
            self.request_history[client_id] = []
        
        # Clean old requests (older than 1 minute)
        self.request_history[client_id] = [
            t for t in self.request_history[client_id]
            if current_time - t < 60
        ]
        
        # Check if over limit
        if len(self.request_history[client_id]) >= self.requests_per_minute:
            return JSONResponse(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                content={"detail": "Rate limit exceeded"}
            )
        
        # Record request
        self.request_history[client_id].append(current_time)
        
        response = await call_next(request)
        
        # Add rate limit headers
        response.headers["X-RateLimit-Limit"] = str(self.requests_per_minute)
        response.headers["X-RateLimit-Remaining"] = str(
            self.requests_per_minute - len(self.request_history[client_id])
        )
        
        return response


class CORSMiddleware:
    """Custom CORS middleware for development"""
    
    def __init__(self, app):
        self.app = app
        self.allowed_origins = [
            "http://localhost:3000",
            "http://localhost:8000",
            "https://localhost:3000",
            "http://127.0.0.1:3000",
        ]
    
    async def __call__(self, request: Request, call_next):
        """Handle CORS for requests"""
        origin = request.headers.get("origin")
        
        if origin in self.allowed_origins or origin is None:
            response = await call_next(request)
            
            # Add CORS headers
            response.headers["Access-Control-Allow-Origin"] = origin or "*"
            response.headers["Access-Control-Allow-Credentials"] = "true"
            response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
            response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
            
            return response
        
        return await call_next(request)


def get_token_from_request(request: Request) -> Optional[str]:
    """Extract JWT token from request"""
    auth_header = request.headers.get("Authorization")
    if auth_header:
        try:
            scheme, credentials = auth_header.split()
            if scheme.lower() == "bearer":
                return credentials
        except ValueError:
            pass
    return None


def require_auth(request: Request):
    """Dependency to require authentication"""
    if not getattr(request.state, "authenticated", False):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return getattr(request.state, "user_id", None)


def require_permission(required_permissions: list):
    """Dependency factory to require specific permissions"""
    async def _require_permission(request: Request):
        if not getattr(request.state, "authenticated", False):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authentication required",
            )
        
        auth = get_auth_service()
        user_id = getattr(request.state, "user_id", None)
        user = auth.get_user(user_id)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found",
            )
        
        # Check permissions
        has_permission = False
        for permission in required_permissions:
            if PermissionManager.has_permission(user, permission):
                has_permission = True
                break
        
        if not has_permission:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions",
            )
        
        return user
    
    return _require_permission


if __name__ == "__main__":
    print("Authentication and Authorization Middleware Module")
    print("\nFeatures:")
    print("- JWT token extraction and validation")
    print("- Permission-based access control")
    print("- Rate limiting")
    print("- CORS support")
    print("- Dependency injection for auth checks")
