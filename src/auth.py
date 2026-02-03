"""
User authentication and authorization module for CuratAI.
Handles user registration, login, token generation, and permission management.
"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Optional, Dict, Set
from enum import Enum
import secrets
import hashlib
import json
from pathlib import Path

try:
    from jwt import encode, decode, ExpiredSignatureError, InvalidTokenError
except ImportError:
    encode = decode = None
    ExpiredSignatureError = InvalidTokenError = Exception

from uuid import uuid4


class UserRole(Enum):
    """User roles in the system"""
    ARTIST = "artist"
    CURATOR = "curator"
    ADMIN = "admin"


class SubscriptionTier(Enum):
    """User subscription tiers"""
    FREE = "free"  # 10 opportunities/month, basic features
    PRO = "pro"  # Unlimited opportunities, AI generation
    ENTERPRISE = "enterprise"  # All features + priority support


@dataclass
class Permission:
    """Permission for actions in the system"""
    resource: str  # 'opportunities', 'proposals', 'users', etc.
    action: str  # 'read', 'write', 'delete', 'admin'
    tier_required: Optional[SubscriptionTier] = None


@dataclass
class UserAccount:
    """User account with authentication and permissions"""
    user_id: str = field(default_factory=lambda: str(uuid4()))
    email: str = ""
    artist_name: str = ""
    password_hash: str = ""
    role: UserRole = UserRole.ARTIST
    subscription_tier: SubscriptionTier = SubscriptionTier.FREE
    verified: bool = False
    verification_token: Optional[str] = None
    reset_token: Optional[str] = None
    reset_token_expires: Optional[datetime] = None
    created_at: datetime = field(default_factory=datetime.utcnow)
    last_login: Optional[datetime] = None
    avatar_url: Optional[str] = None
    bio: Optional[str] = None
    active: bool = True
    
    # Permissions
    permissions: Set[str] = field(default_factory=set)
    
    # Security
    login_attempts: int = 0
    locked_until: Optional[datetime] = None


@dataclass
class AuthToken:
    """JWT authentication token"""
    access_token: str
    token_type: str = "bearer"
    expires_in: int = 3600  # 1 hour
    refresh_token: Optional[str] = None
    user_id: str = ""


class PasswordManager:
    """Secure password hashing and verification"""
    
    @staticmethod
    def hash_password(password: str, salt: str = None) -> tuple[str, str]:
        """
        Hash password with salt
        
        Args:
            password: Plain text password
            salt: Optional salt, generates if not provided
            
        Returns:
            (hash, salt) tuple
        """
        if not salt:
            salt = secrets.token_hex(16)
        
        password_hash = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            salt.encode('utf-8'),
            100000
        ).hex()
        
        return password_hash, salt
    
    @staticmethod
    def verify_password(password: str, password_hash: str, salt: str) -> bool:
        """Verify password against hash"""
        computed_hash, _ = PasswordManager.hash_password(password, salt)
        return secrets.compare_digest(computed_hash, password_hash)


class TokenManager:
    """JWT token generation and validation"""
    
    def __init__(self, secret_key: str = None, algorithm: str = "HS256"):
        """
        Initialize token manager
        
        Args:
            secret_key: Secret key for signing (generates if not provided)
            algorithm: JWT algorithm
        """
        self.secret_key = secret_key or secrets.token_urlsafe(32)
        self.algorithm = algorithm
        self.access_token_expire_minutes = 60
        self.refresh_token_expire_days = 7
    
    def create_access_token(self, user_id: str, user_email: str) -> str:
        """Create JWT access token"""
        if not encode:
            raise RuntimeError("PyJWT not installed. Install with: pip install PyJWT")
        
        payload = {
            "sub": user_id,
            "email": user_email,
            "exp": datetime.utcnow() + timedelta(minutes=self.access_token_expire_minutes),
            "iat": datetime.utcnow(),
            "type": "access"
        }
        
        return encode(payload, self.secret_key, algorithm=self.algorithm)
    
    def create_refresh_token(self, user_id: str) -> str:
        """Create JWT refresh token"""
        if not encode:
            raise RuntimeError("PyJWT not installed")
        
        payload = {
            "sub": user_id,
            "exp": datetime.utcnow() + timedelta(days=self.refresh_token_expire_days),
            "iat": datetime.utcnow(),
            "type": "refresh"
        }
        
        return encode(payload, self.secret_key, algorithm=self.algorithm)
    
    def verify_token(self, token: str) -> Dict:
        """Verify and decode token"""
        if not decode:
            raise RuntimeError("PyJWT not installed")
        
        try:
            payload = decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except ExpiredSignatureError:
            raise ValueError("Token expired")
        except InvalidTokenError:
            raise ValueError("Invalid token")


class PermissionManager:
    """Manage user permissions based on role and subscription"""
    
    # Define permissions for each role
    ROLE_PERMISSIONS = {
        UserRole.ARTIST: {
            "opportunities:read",
            "opportunities:track",
            "proposals:create",
            "proposals:read",
            "proposals:update",
            "proposals:submit",
            "profile:read",
            "profile:update",
            "notifications:read",
        },
        UserRole.CURATOR: {
            "opportunities:read",
            "opportunities:create",
            "opportunities:update",
            "opportunities:delete",
            "opportunities:track",
            "proposals:read",
            "proposals:evaluate",
            "users:read",
            "profile:read",
            "profile:update",
            "notifications:read",
        },
        UserRole.ADMIN: {
            "opportunities:*",
            "proposals:*",
            "users:*",
            "admin:*",
        }
    }
    
    # Premium features by tier
    TIER_FEATURES = {
        SubscriptionTier.FREE: {
            "max_opportunities_per_month": 10,
            "ai_generation": False,
            "priority_support": False,
        },
        SubscriptionTier.PRO: {
            "max_opportunities_per_month": 100,
            "ai_generation": True,
            "priority_support": False,
        },
        SubscriptionTier.ENTERPRISE: {
            "max_opportunities_per_month": -1,  # Unlimited
            "ai_generation": True,
            "priority_support": True,
        }
    }
    
    @staticmethod
    def get_role_permissions(role: UserRole) -> Set[str]:
        """Get all permissions for a role"""
        return PermissionManager.ROLE_PERMISSIONS.get(role, set())
    
    @staticmethod
    def has_permission(user: UserAccount, permission: str) -> bool:
        """Check if user has permission"""
        if user.role == UserRole.ADMIN:
            return True  # Admins have all permissions
        
        return permission in user.permissions
    
    @staticmethod
    def check_tier_feature(tier: SubscriptionTier, feature: str) -> bool:
        """Check if tier has feature"""
        features = PermissionManager.TIER_FEATURES.get(tier, {})
        return features.get(feature, False)


class AuthenticationService:
    """Main authentication service"""
    
    def __init__(self, secret_key: str = None):
        """
        Initialize auth service
        
        Args:
            secret_key: Secret for token signing
        """
        self.token_manager = TokenManager(secret_key)
        self.password_manager = PasswordManager()
        self.users: Dict[str, UserAccount] = {}
        self.email_to_user: Dict[str, str] = {}
        self.refresh_tokens: Dict[str, str] = {}
        
        # Simulated storage
        self.users_file = Path("users_data.json")
        self._load_users()
    
    def _load_users(self):
        """Load users from file if exists"""
        if self.users_file.exists():
            try:
                with open(self.users_file, 'r') as f:
                    data = json.load(f)
                    for user_data in data.get('users', []):
                        user = self._deserialize_user(user_data)
                        self.users[user.user_id] = user
                        self.email_to_user[user.email] = user.user_id
            except Exception as e:
                print(f"Error loading users: {e}")
    
    def _save_users(self):
        """Save users to file"""
        try:
            data = {
                'users': [self._serialize_user(user) for user in self.users.values()]
            }
            with open(self.users_file, 'w') as f:
                json.dump(data, f, indent=2, default=str)
        except Exception as e:
            print(f"Error saving users: {e}")
    
    def _serialize_user(self, user: UserAccount) -> Dict:
        """Serialize user to dict"""
        return {
            'user_id': user.user_id,
            'email': user.email,
            'artist_name': user.artist_name,
            'password_hash': user.password_hash,
            'role': user.role.value,
            'subscription_tier': user.subscription_tier.value,
            'verified': user.verified,
            'avatar_url': user.avatar_url,
            'bio': user.bio,
            'active': user.active,
            'created_at': user.created_at.isoformat(),
            'last_login': user.last_login.isoformat() if user.last_login else None,
        }
    
    def _deserialize_user(self, data: Dict) -> UserAccount:
        """Deserialize user from dict"""
        user = UserAccount(
            user_id=data['user_id'],
            email=data['email'],
            artist_name=data['artist_name'],
            password_hash=data['password_hash'],
            role=UserRole(data['role']),
            subscription_tier=SubscriptionTier(data['subscription_tier']),
            verified=data['verified'],
            avatar_url=data.get('avatar_url'),
            bio=data.get('bio'),
            active=data.get('active', True),
            created_at=datetime.fromisoformat(data['created_at']),
        )
        
        # Set permissions based on role
        user.permissions = PermissionManager.get_role_permissions(user.role)
        
        if data.get('last_login'):
            user.last_login = datetime.fromisoformat(data['last_login'])
        
        return user
    
    def register(self, email: str, password: str, artist_name: str) -> UserAccount:
        """
        Register new user
        
        Args:
            email: User email
            password: User password
            artist_name: Artist display name
            
        Returns:
            UserAccount
            
        Raises:
            ValueError: If email already registered
        """
        if email.lower() in self.email_to_user:
            raise ValueError(f"Email {email} already registered")
        
        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters")
        
        # Create user
        user = UserAccount(
            email=email.lower(),
            artist_name=artist_name,
            subscription_tier=SubscriptionTier.FREE,
        )
        
        # Hash password
        password_hash, salt = self.password_manager.hash_password(password)
        user.password_hash = f"{password_hash}${salt}"
        
        # Set permissions
        user.permissions = PermissionManager.get_role_permissions(user.role)
        
        # Generate verification token
        user.verification_token = secrets.token_urlsafe(32)
        
        # Save user
        self.users[user.user_id] = user
        self.email_to_user[user.email] = user.user_id
        self._save_users()
        
        return user
    
    def login(self, email: str, password: str) -> AuthToken:
        """
        Authenticate user and return token
        
        Args:
            email: User email
            password: User password
            
        Returns:
            AuthToken
            
        Raises:
            ValueError: If credentials invalid
        """
        email = email.lower()
        
        if email not in self.email_to_user:
            raise ValueError("Invalid email or password")
        
        user = self.users[self.email_to_user[email]]
        
        if not user.active:
            raise ValueError("Account is disabled")
        
        # Check account lock
        if user.locked_until and user.locked_until > datetime.utcnow():
            raise ValueError("Account temporarily locked. Try again later")
        
        # Verify password
        if '$' not in user.password_hash:
            raise ValueError("Invalid credentials")
        
        password_hash, salt = user.password_hash.split('$')
        if not self.password_manager.verify_password(password, password_hash, salt):
            user.login_attempts += 1
            
            # Lock after 5 failed attempts
            if user.login_attempts >= 5:
                user.locked_until = datetime.utcnow() + timedelta(minutes=15)
            
            self._save_users()
            raise ValueError("Invalid email or password")
        
        # Reset login attempts
        user.login_attempts = 0
        user.locked_until = None
        user.last_login = datetime.utcnow()
        self._save_users()
        
        # Generate tokens
        access_token = self.token_manager.create_access_token(user.user_id, user.email)
        refresh_token = self.token_manager.create_refresh_token(user.user_id)
        
        # Store refresh token
        self.refresh_tokens[refresh_token] = user.user_id
        
        return AuthToken(
            access_token=access_token,
            refresh_token=refresh_token,
            user_id=user.user_id,
            expires_in=3600,
        )
    
    def verify_token(self, token: str) -> Dict:
        """Verify JWT token"""
        return self.token_manager.verify_token(token)
    
    def refresh_access_token(self, refresh_token: str) -> AuthToken:
        """Create new access token from refresh token"""
        if refresh_token not in self.refresh_tokens:
            raise ValueError("Invalid refresh token")
        
        user_id = self.refresh_tokens[refresh_token]
        user = self.users.get(user_id)
        
        if not user:
            raise ValueError("User not found")
        
        # Verify refresh token
        self.token_manager.verify_token(refresh_token)
        
        # Create new access token
        access_token = self.token_manager.create_access_token(user.user_id, user.email)
        
        return AuthToken(
            access_token=access_token,
            refresh_token=refresh_token,
            user_id=user.user_id,
            expires_in=3600,
        )
    
    def logout(self, refresh_token: str):
        """Logout user by invalidating refresh token"""
        if refresh_token in self.refresh_tokens:
            del self.refresh_tokens[refresh_token]
    
    def get_user(self, user_id: str) -> Optional[UserAccount]:
        """Get user by ID"""
        return self.users.get(user_id)
    
    def get_user_by_email(self, email: str) -> Optional[UserAccount]:
        """Get user by email"""
        email = email.lower()
        user_id = self.email_to_user.get(email)
        return self.users.get(user_id) if user_id else None
    
    def upgrade_subscription(self, user_id: str, tier: SubscriptionTier) -> UserAccount:
        """Upgrade user subscription"""
        user = self.users.get(user_id)
        if not user:
            raise ValueError("User not found")
        
        user.subscription_tier = tier
        self._save_users()
        return user
    
    def verify_email(self, user_id: str, verification_token: str) -> UserAccount:
        """Verify user email"""
        user = self.users.get(user_id)
        if not user:
            raise ValueError("User not found")
        
        if user.verification_token != verification_token:
            raise ValueError("Invalid verification token")
        
        user.verified = True
        user.verification_token = None
        self._save_users()
        return user
    
    def request_password_reset(self, email: str) -> str:
        """Generate password reset token"""
        user = self.get_user_by_email(email)
        if not user:
            raise ValueError("User not found")
        
        user.reset_token = secrets.token_urlsafe(32)
        user.reset_token_expires = datetime.utcnow() + timedelta(hours=1)
        self._save_users()
        
        return user.reset_token
    
    def reset_password(self, email: str, reset_token: str, new_password: str) -> UserAccount:
        """Reset user password"""
        user = self.get_user_by_email(email)
        if not user:
            raise ValueError("User not found")
        
        if user.reset_token != reset_token:
            raise ValueError("Invalid reset token")
        
        if user.reset_token_expires and user.reset_token_expires < datetime.utcnow():
            raise ValueError("Reset token expired")
        
        if len(new_password) < 8:
            raise ValueError("Password must be at least 8 characters")
        
        # Hash new password
        password_hash, salt = self.password_manager.hash_password(new_password)
        user.password_hash = f"{password_hash}${salt}"
        user.reset_token = None
        user.reset_token_expires = None
        self._save_users()
        
        return user


# Global auth service instance
_auth_service: Optional[AuthenticationService] = None


def get_auth_service() -> AuthenticationService:
    """Get global auth service instance"""
    global _auth_service
    if _auth_service is None:
        _auth_service = AuthenticationService()
    return _auth_service


if __name__ == "__main__":
    # Demo usage
    auth = get_auth_service()
    
    # Register user
    try:
        user = auth.register("artist@example.com", "SecurePassword123", "Test Artist")
        print(f"✅ Registered: {user.artist_name} ({user.user_id})")
        print(f"   Email verified: {user.verified}")
        print(f"   Permissions: {user.permissions}")
    except ValueError as e:
        print(f"Registration error: {e}")
    
    # Login
    try:
        token = auth.login("artist@example.com", "SecurePassword123")
        print(f"\n✅ Login successful")
        print(f"   Access token: {token.access_token[:20]}...")
        print(f"   Expires in: {token.expires_in}s")
        
        # Verify token
        payload = auth.verify_token(token.access_token)
        print(f"\n✅ Token verified")
        print(f"   User ID: {payload.get('sub')}")
        print(f"   Email: {payload.get('email')}")
        print(f"   Token type: {payload.get('type')}")
    except ValueError as e:
        print(f"Login error: {e}")
    
    # Check permissions
    user = auth.get_user_by_email("artist@example.com")
    if user:
        print(f"\n✅ User permissions:")
        for perm in sorted(user.permissions):
            print(f"   - {perm}")
    
    # Upgrade subscription
    try:
        upgraded_user = auth.upgrade_subscription(user.user_id, SubscriptionTier.PRO)
        print(f"\n✅ Upgraded to {upgraded_user.subscription_tier.value}")
        
        can_generate = PermissionManager.check_tier_feature(upgraded_user.subscription_tier, "ai_generation")
        print(f"   AI generation enabled: {can_generate}")
    except ValueError as e:
        print(f"Upgrade error: {e}")
