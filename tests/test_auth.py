"""
Integration tests for authentication and authorization system.
Tests user registration, login, token management, and permissions.
"""

import pytest
from datetime import datetime, timedelta
from auth import (
    AuthenticationService,
    PasswordManager,
    TokenManager,
    PermissionManager,
    UserRole,
    SubscriptionTier,
    UserAccount,
)


class TestPasswordManager:
    """Test password hashing and verification"""
    
    def test_hash_password_creates_hash_and_salt(self):
        """Test password hashing with salt generation"""
        password = "TestPassword123"
        password_hash, salt = PasswordManager.hash_password(password)
        
        assert password_hash
        assert salt
        assert len(password_hash) == 64  # SHA256 hex
        assert len(salt) >= 16
    
    def test_verify_password_success(self):
        """Test successful password verification"""
        password = "TestPassword123"
        password_hash, salt = PasswordManager.hash_password(password)
        
        assert PasswordManager.verify_password(password, password_hash, salt)
    
    def test_verify_password_failure(self):
        """Test failed password verification with wrong password"""
        password = "TestPassword123"
        wrong_password = "WrongPassword123"
        password_hash, salt = PasswordManager.hash_password(password)
        
        assert not PasswordManager.verify_password(wrong_password, password_hash, salt)
    
    def test_hash_with_custom_salt(self):
        """Test password hashing with provided salt"""
        password = "TestPassword123"
        salt = "fixed_salt_value"
        password_hash, returned_salt = PasswordManager.hash_password(password, salt)
        
        assert returned_salt == salt
        assert PasswordManager.verify_password(password, password_hash, salt)


class TestTokenManager:
    """Test JWT token generation and validation"""
    
    def test_create_access_token(self):
        """Test access token creation"""
        tm = TokenManager()
        token = tm.create_access_token("user123", "user@example.com")
        
        assert token
        assert isinstance(token, str)
        assert len(token.split('.')) == 3  # JWT format: header.payload.signature
    
    def test_create_refresh_token(self):
        """Test refresh token creation"""
        tm = TokenManager()
        token = tm.create_refresh_token("user123")
        
        assert token
        assert isinstance(token, str)
    
    def test_verify_access_token(self):
        """Test token verification"""
        tm = TokenManager()
        user_id = "user123"
        email = "user@example.com"
        
        token = tm.create_access_token(user_id, email)
        payload = tm.verify_token(token)
        
        assert payload["sub"] == user_id
        assert payload["email"] == email
        assert payload["type"] == "access"
    
    def test_verify_invalid_token(self):
        """Test verification of invalid token"""
        tm = TokenManager()
        
        with pytest.raises(ValueError):
            tm.verify_token("invalid.token.here")


class TestPermissionManager:
    """Test permission and authorization logic"""
    
    def test_artist_permissions(self):
        """Test artist role has correct permissions"""
        artist_permissions = PermissionManager.get_role_permissions(UserRole.ARTIST)
        
        assert "opportunities:read" in artist_permissions
        assert "proposals:create" in artist_permissions
        assert "proposals:submit" in artist_permissions
        assert "admin:*" not in artist_permissions
    
    def test_curator_permissions(self):
        """Test curator role has correct permissions"""
        curator_permissions = PermissionManager.get_role_permissions(UserRole.CURATOR)
        
        assert "opportunities:read" in curator_permissions
        assert "opportunities:create" in curator_permissions
        assert "proposals:evaluate" in curator_permissions
    
    def test_admin_permissions(self):
        """Test admin has all permissions"""
        admin_permissions = PermissionManager.get_role_permissions(UserRole.ADMIN)
        
        assert "opportunities:*" in admin_permissions
        assert "users:*" in admin_permissions
        assert "admin:*" in admin_permissions
    
    def test_admin_has_all_permissions(self):
        """Test admin user has any permission"""
        admin = UserAccount(role=UserRole.ADMIN)
        admin.permissions = PermissionManager.get_role_permissions(UserRole.ADMIN)
        
        assert PermissionManager.has_permission(admin, "anything:here")
    
    def test_artist_lacks_admin_permission(self):
        """Test artist cannot access admin functions"""
        artist = UserAccount(role=UserRole.ARTIST)
        artist.permissions = PermissionManager.get_role_permissions(UserRole.ARTIST)
        
        assert not PermissionManager.has_permission(artist, "admin:panel")
    
    def test_tier_features(self):
        """Test subscription tier features"""
        free_features = PermissionManager.TIER_FEATURES[SubscriptionTier.FREE]
        pro_features = PermissionManager.TIER_FEATURES[SubscriptionTier.PRO]
        
        assert free_features["ai_generation"] == False
        assert pro_features["ai_generation"] == True
        
        assert free_features["max_opportunities_per_month"] == 10
        assert pro_features["max_opportunities_per_month"] == 100


class TestAuthenticationService:
    """Test main authentication service"""
    
    @pytest.fixture
    def auth_service(self):
        """Create fresh auth service for each test"""
        return AuthenticationService(secret_key="test_secret_key")
    
    def test_register_new_user(self, auth_service):
        """Test user registration"""
        user = auth_service.register(
            email="newuser@example.com",
            password="SecurePassword123",
            artist_name="Test Artist"
        )
        
        assert user.user_id
        assert user.email == "newuser@example.com"
        assert user.artist_name == "Test Artist"
        assert user.role == UserRole.ARTIST
        assert user.subscription_tier == SubscriptionTier.FREE
        assert not user.verified
    
    def test_register_duplicate_email(self, auth_service):
        """Test registration fails with duplicate email"""
        auth_service.register(
            email="user@example.com",
            password="SecurePassword123",
            artist_name="First Artist"
        )
        
        with pytest.raises(ValueError):
            auth_service.register(
                email="user@example.com",
                password="SecurePassword123",
                artist_name="Second Artist"
            )
    
    def test_register_weak_password(self, auth_service):
        """Test registration fails with weak password"""
        with pytest.raises(ValueError):
            auth_service.register(
                email="user@example.com",
                password="weak",
                artist_name="Artist"
            )
    
    def test_login_success(self, auth_service):
        """Test successful login"""
        auth_service.register(
            email="user@example.com",
            password="SecurePassword123",
            artist_name="Test Artist"
        )
        
        token = auth_service.login("user@example.com", "SecurePassword123")
        
        assert token.access_token
        assert token.refresh_token
        assert token.user_id
        assert token.expires_in == 3600
    
    def test_login_wrong_password(self, auth_service):
        """Test login fails with wrong password"""
        auth_service.register(
            email="user@example.com",
            password="SecurePassword123",
            artist_name="Test Artist"
        )
        
        with pytest.raises(ValueError):
            auth_service.login("user@example.com", "WrongPassword123")
    
    def test_login_nonexistent_user(self, auth_service):
        """Test login fails for nonexistent user"""
        with pytest.raises(ValueError):
            auth_service.login("nonexistent@example.com", "password")
    
    def test_login_account_lock(self, auth_service):
        """Test account lockout after failed attempts"""
        auth_service.register(
            email="user@example.com",
            password="SecurePassword123",
            artist_name="Test Artist"
        )
        
        # Make 5 failed attempts
        for _ in range(5):
            try:
                auth_service.login("user@example.com", "WrongPassword")
            except ValueError:
                pass
        
        # 6th attempt should fail with locked account
        user = auth_service.get_user_by_email("user@example.com")
        assert user.locked_until is not None
    
    def test_verify_token_success(self, auth_service):
        """Test token verification"""
        auth_service.register(
            email="user@example.com",
            password="SecurePassword123",
            artist_name="Test Artist"
        )
        
        token_data = auth_service.login("user@example.com", "SecurePassword123")
        payload = auth_service.verify_token(token_data.access_token)
        
        assert payload["sub"] == token_data.user_id
        assert payload["email"] == "user@example.com"
    
    def test_refresh_token(self, auth_service):
        """Test token refresh"""
        auth_service.register(
            email="user@example.com",
            password="SecurePassword123",
            artist_name="Test Artist"
        )
        
        token_data = auth_service.login("user@example.com", "SecurePassword123")
        new_token = auth_service.refresh_access_token(token_data.refresh_token)
        
        assert new_token.access_token
        assert new_token.access_token != token_data.access_token
    
    def test_logout(self, auth_service):
        """Test logout invalidates refresh token"""
        auth_service.register(
            email="user@example.com",
            password="SecurePassword123",
            artist_name="Test Artist"
        )
        
        token_data = auth_service.login("user@example.com", "SecurePassword123")
        auth_service.logout(token_data.refresh_token)
        
        with pytest.raises(ValueError):
            auth_service.refresh_access_token(token_data.refresh_token)
    
    def test_get_user(self, auth_service):
        """Test retrieving user by ID"""
        user = auth_service.register(
            email="user@example.com",
            password="SecurePassword123",
            artist_name="Test Artist"
        )
        
        retrieved_user = auth_service.get_user(user.user_id)
        
        assert retrieved_user.user_id == user.user_id
        assert retrieved_user.email == user.email
    
    def test_get_user_by_email(self, auth_service):
        """Test retrieving user by email"""
        user = auth_service.register(
            email="user@example.com",
            password="SecurePassword123",
            artist_name="Test Artist"
        )
        
        retrieved_user = auth_service.get_user_by_email("user@example.com")
        
        assert retrieved_user.user_id == user.user_id
    
    def test_upgrade_subscription(self, auth_service):
        """Test subscription upgrade"""
        user = auth_service.register(
            email="user@example.com",
            password="SecurePassword123",
            artist_name="Test Artist"
        )
        
        upgraded_user = auth_service.upgrade_subscription(
            user.user_id,
            SubscriptionTier.PRO
        )
        
        assert upgraded_user.subscription_tier == SubscriptionTier.PRO
    
    def test_verify_email(self, auth_service):
        """Test email verification"""
        user = auth_service.register(
            email="user@example.com",
            password="SecurePassword123",
            artist_name="Test Artist"
        )
        
        assert not user.verified
        verification_token = user.verification_token
        
        verified_user = auth_service.verify_email(user.user_id, verification_token)
        
        assert verified_user.verified
        assert verified_user.verification_token is None
    
    def test_password_reset(self, auth_service):
        """Test password reset flow"""
        auth_service.register(
            email="user@example.com",
            password="OldPassword123",
            artist_name="Test Artist"
        )
        
        # Request reset
        reset_token = auth_service.request_password_reset("user@example.com")
        assert reset_token
        
        # Confirm reset
        user = auth_service.reset_password(
            email="user@example.com",
            reset_token=reset_token,
            new_password="NewPassword123"
        )
        
        # Login with new password
        token = auth_service.login("user@example.com", "NewPassword123")
        assert token.access_token
    
    def test_password_reset_invalid_token(self, auth_service):
        """Test password reset with invalid token"""
        auth_service.register(
            email="user@example.com",
            password="SecurePassword123",
            artist_name="Test Artist"
        )
        
        with pytest.raises(ValueError):
            auth_service.reset_password(
                email="user@example.com",
                reset_token="invalid_token",
                new_password="NewPassword123"
            )


class TestUserPermissionIntegration:
    """Integration tests for user roles and permissions"""
    
    def test_artist_workflow(self):
        """Test complete artist user workflow"""
        auth = AuthenticationService()
        
        # Register
        user = auth.register(
            email="artist@example.com",
            password="ArtistPassword123",
            artist_name="Creative Artist"
        )
        
        # Verify permissions
        assert PermissionManager.has_permission(user, "opportunities:read")
        assert PermissionManager.has_permission(user, "proposals:create")
        assert not PermissionManager.has_permission(user, "admin:panel")
        
        # Login
        token_data = auth.login("artist@example.com", "ArtistPassword123")
        
        # Verify token
        payload = auth.verify_token(token_data.access_token)
        assert payload["type"] == "access"
        
        # Upgrade to pro
        upgraded_user = auth.upgrade_subscription(user.user_id, SubscriptionTier.PRO)
        assert upgraded_user.subscription_tier == SubscriptionTier.PRO


# Run tests
if __name__ == "__main__":
    pytest.main([__file__, "-v"])
