"""Tests for SMTP Users builder."""

import pytest

from mailersend.builders.smtp_users import SmtpUsersBuilder
from mailersend.models.smtp_users import (
    SmtpUsersListRequest, SmtpUserGetRequest, SmtpUserCreateRequest,
    SmtpUserUpdateRequest, SmtpUserDeleteRequest
)
from mailersend.exceptions import ValidationError


class TestSmtpUsersBuilderBasicMethods:
    """Test basic SmtpUsersBuilder methods."""
    
    def test_initialization(self):
        """Test SmtpUsersBuilder initialization."""
        builder = SmtpUsersBuilder()
        
        assert builder._domain_id is None
        assert builder._smtp_user_id is None
        assert builder._name is None
        assert builder._enabled is None
        assert builder._page == 1
        assert builder._limit == 25
    
    def test_domain_id_method(self):
        """Test domain_id method."""
        builder = SmtpUsersBuilder()
        result = builder.domain_id("test-domain")
        
        assert result is builder  # Method chaining
        assert builder._domain_id == "test-domain"
    
    def test_smtp_user_id_method(self):
        """Test smtp_user_id method."""
        builder = SmtpUsersBuilder()
        result = builder.smtp_user_id("user123")
        
        assert result is builder  # Method chaining
        assert builder._smtp_user_id == "user123"
    
    def test_name_method(self):
        """Test name method."""
        builder = SmtpUsersBuilder()
        result = builder.name("Test User")
        
        assert result is builder  # Method chaining
        assert builder._name == "Test User"
    
    def test_enabled_method(self):
        """Test enabled method."""
        builder = SmtpUsersBuilder()
        result = builder.enabled(True)
        
        assert result is builder  # Method chaining
        assert builder._enabled is True
    
    def test_page_method(self):
        """Test page method."""
        builder = SmtpUsersBuilder()
        result = builder.page(2)
        
        assert result is builder  # Method chaining
        assert builder._page == 2
    
    def test_page_method_validation(self):
        """Test page method validation."""
        builder = SmtpUsersBuilder()
        
        with pytest.raises(ValidationError, match="Page must be >= 1"):
            builder.page(0)
        
        with pytest.raises(ValidationError, match="Page must be >= 1"):
            builder.page(-1)
        
        # Valid page numbers should work
        builder.page(1)
        assert builder._page == 1
    
    def test_limit_method(self):
        """Test limit method."""
        builder = SmtpUsersBuilder()
        result = builder.limit(50)
        
        assert result is builder  # Method chaining
        assert builder._limit == 50
    
    def test_limit_method_validation(self):
        """Test limit method validation."""
        builder = SmtpUsersBuilder()
        
        with pytest.raises(ValidationError, match="Limit must be between 10 and 100"):
            builder.limit(5)
        
        with pytest.raises(ValidationError, match="Limit must be between 10 and 100"):
            builder.limit(150)
        
        # Valid limits should work
        builder.limit(10)
        assert builder._limit == 10
        
        builder.limit(100)
        assert builder._limit == 100


class TestSmtpUsersBuilderBuildMethods:
    """Test SmtpUsersBuilder build methods."""
    
    def test_build_smtp_users_list_basic(self):
        """Test build_smtp_users_list with basic setup."""
        builder = SmtpUsersBuilder()
        builder.domain_id("test-domain")
        
        request = builder.build_smtp_users_list()
        
        assert isinstance(request, SmtpUsersListRequest)
        assert request.domain_id == "test-domain"
        assert request.query_params.limit == 25
    
    def test_build_smtp_users_list_with_limit(self):
        """Test build_smtp_users_list with custom limit."""
        builder = SmtpUsersBuilder()
        builder.domain_id("test-domain").limit(50)
        
        request = builder.build_smtp_users_list()
        
        assert isinstance(request, SmtpUsersListRequest)
        assert request.domain_id == "test-domain"
        assert request.query_params.limit == 50
    
    def test_build_smtp_users_list_missing_domain_id(self):
        """Test build_smtp_users_list validation when domain_id is missing."""
        builder = SmtpUsersBuilder()
        
        with pytest.raises(ValidationError, match="Domain ID is required"):
            builder.build_smtp_users_list()
    
    def test_build_smtp_user_get_success(self):
        """Test build_smtp_user_get with valid data."""
        builder = SmtpUsersBuilder()
        builder.domain_id("test-domain").smtp_user_id("user123")
        
        request = builder.build_smtp_user_get()
        
        assert isinstance(request, SmtpUserGetRequest)
        assert request.domain_id == "test-domain"
        assert request.smtp_user_id == "user123"
    
    def test_build_smtp_user_get_missing_domain_id(self):
        """Test build_smtp_user_get validation when domain_id is missing."""
        builder = SmtpUsersBuilder()
        builder.smtp_user_id("user123")
        
        with pytest.raises(ValidationError, match="Domain ID is required"):
            builder.build_smtp_user_get()
    
    def test_build_smtp_user_get_missing_smtp_user_id(self):
        """Test build_smtp_user_get validation when smtp_user_id is missing."""
        builder = SmtpUsersBuilder()
        builder.domain_id("test-domain")
        
        with pytest.raises(ValidationError, match="SMTP User ID is required"):
            builder.build_smtp_user_get()
    
    def test_build_smtp_user_create_success(self):
        """Test build_smtp_user_create with valid data."""
        builder = SmtpUsersBuilder()
        builder.domain_id("test-domain").name("Test User")
        
        request = builder.build_smtp_user_create()
        
        assert isinstance(request, SmtpUserCreateRequest)
        assert request.domain_id == "test-domain"
        assert request.name == "Test User"
        assert request.enabled is None
    
    def test_build_smtp_user_create_with_enabled(self):
        """Test build_smtp_user_create with enabled flag."""
        builder = SmtpUsersBuilder()
        builder.domain_id("test-domain").name("Test User").enabled(True)
        
        request = builder.build_smtp_user_create()
        
        assert isinstance(request, SmtpUserCreateRequest)
        assert request.domain_id == "test-domain"
        assert request.name == "Test User"
        assert request.enabled is True
    
    def test_build_smtp_user_create_missing_domain_id(self):
        """Test build_smtp_user_create validation when domain_id is missing."""
        builder = SmtpUsersBuilder()
        builder.name("Test User")
        
        with pytest.raises(ValidationError, match="Domain ID is required"):
            builder.build_smtp_user_create()
    
    def test_build_smtp_user_create_missing_name(self):
        """Test build_smtp_user_create validation when name is missing."""
        builder = SmtpUsersBuilder()
        builder.domain_id("test-domain")
        
        with pytest.raises(ValidationError, match="Name is required"):
            builder.build_smtp_user_create()
    
    def test_build_smtp_user_update_success(self):
        """Test build_smtp_user_update with valid data."""
        builder = SmtpUsersBuilder()
        builder.domain_id("test-domain").smtp_user_id("user123").name("Updated User")
        
        request = builder.build_smtp_user_update()
        
        assert isinstance(request, SmtpUserUpdateRequest)
        assert request.domain_id == "test-domain"
        assert request.smtp_user_id == "user123"
        assert request.name == "Updated User"
        assert request.enabled is None
    
    def test_build_smtp_user_update_with_enabled(self):
        """Test build_smtp_user_update with enabled flag."""
        builder = SmtpUsersBuilder()
        builder.domain_id("test-domain").smtp_user_id("user123").name("Updated User").enabled(False)
        
        request = builder.build_smtp_user_update()
        
        assert isinstance(request, SmtpUserUpdateRequest)
        assert request.domain_id == "test-domain"
        assert request.smtp_user_id == "user123"
        assert request.name == "Updated User"
        assert request.enabled is False
    
    def test_build_smtp_user_update_missing_domain_id(self):
        """Test build_smtp_user_update validation when domain_id is missing."""
        builder = SmtpUsersBuilder()
        builder.smtp_user_id("user123").name("Updated User")
        
        with pytest.raises(ValidationError, match="Domain ID is required"):
            builder.build_smtp_user_update()
    
    def test_build_smtp_user_update_missing_smtp_user_id(self):
        """Test build_smtp_user_update validation when smtp_user_id is missing."""
        builder = SmtpUsersBuilder()
        builder.domain_id("test-domain").name("Updated User")
        
        with pytest.raises(ValidationError, match="SMTP User ID is required"):
            builder.build_smtp_user_update()
    
    def test_build_smtp_user_update_missing_name(self):
        """Test build_smtp_user_update validation when name is missing."""
        builder = SmtpUsersBuilder()
        builder.domain_id("test-domain").smtp_user_id("user123")
        
        with pytest.raises(ValidationError, match="Name is required"):
            builder.build_smtp_user_update()
    
    def test_build_smtp_user_delete_success(self):
        """Test build_smtp_user_delete with valid data."""
        builder = SmtpUsersBuilder()
        builder.domain_id("test-domain").smtp_user_id("user123")
        
        request = builder.build_smtp_user_delete()
        
        assert isinstance(request, SmtpUserDeleteRequest)
        assert request.domain_id == "test-domain"
        assert request.smtp_user_id == "user123"
    
    def test_build_smtp_user_delete_missing_domain_id(self):
        """Test build_smtp_user_delete validation when domain_id is missing."""
        builder = SmtpUsersBuilder()
        builder.smtp_user_id("user123")
        
        with pytest.raises(ValidationError, match="Domain ID is required"):
            builder.build_smtp_user_delete()
    
    def test_build_smtp_user_delete_missing_smtp_user_id(self):
        """Test build_smtp_user_delete validation when smtp_user_id is missing."""
        builder = SmtpUsersBuilder()
        builder.domain_id("test-domain")
        
        with pytest.raises(ValidationError, match="SMTP User ID is required"):
            builder.build_smtp_user_delete() 