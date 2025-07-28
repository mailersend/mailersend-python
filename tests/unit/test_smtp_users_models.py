"""Tests for SMTP Users models."""

import pytest
from datetime import datetime
from pydantic import ValidationError

from mailersend.models.smtp_users import (
    SmtpUsersListQueryParams, SmtpUsersListRequest, SmtpUserGetRequest,
    SmtpUserCreateRequest, SmtpUserUpdateRequest, SmtpUserDeleteRequest,
    SmtpUser, SmtpUsersListResponse, SmtpUserResponse, SmtpUserCreateResponse
)


class TestSmtpUsersListQueryParams:
    """Test SmtpUsersListQueryParams model."""
    
    def test_smtp_users_list_query_params_defaults(self):
        """Test SmtpUsersListQueryParams with default values."""
        params = SmtpUsersListQueryParams()
        
        assert params.limit == 25
    
    def test_smtp_users_list_query_params_custom_values(self):
        """Test SmtpUsersListQueryParams with custom values."""
        params = SmtpUsersListQueryParams(limit=50)
        
        assert params.limit == 50
    
    def test_smtp_users_list_query_params_validation(self):
        """Test SmtpUsersListQueryParams validation."""
        # Test minimum limit
        with pytest.raises(ValidationError):
            SmtpUsersListQueryParams(limit=5)
        
        # Test maximum limit
        with pytest.raises(ValidationError):
            SmtpUsersListQueryParams(limit=150)
        
        # Test valid boundaries
        params_min = SmtpUsersListQueryParams(limit=10)
        assert params_min.limit == 10
        
        params_max = SmtpUsersListQueryParams(limit=100)
        assert params_max.limit == 100
    
    def test_smtp_users_list_query_params_to_query_params_defaults(self):
        """Test to_query_params with default values."""
        params = SmtpUsersListQueryParams()
        result = params.to_query_params()
        
        # Default values should not be included
        assert result == {}
    
    def test_smtp_users_list_query_params_to_query_params_custom(self):
        """Test to_query_params with custom values."""
        params = SmtpUsersListQueryParams(limit=50)
        result = params.to_query_params()
        
        assert result == {"limit": 50}
    
    def test_smtp_users_list_query_params_to_query_params_partial(self):
        """Test to_query_params with partial custom values."""
        params = SmtpUsersListQueryParams(limit=30)
        result = params.to_query_params()
        
        assert result == {"limit": 30}


class TestSmtpUsersListRequest:
    """Test SmtpUsersListRequest model."""
    
    def test_smtp_users_list_request_defaults(self):
        """Test SmtpUsersListRequest with default query params."""
        request = SmtpUsersListRequest(domain_id="test-domain")
        
        assert request.domain_id == "test-domain"
        assert request.query_params.limit == 25
    
    def test_smtp_users_list_request_with_custom_params(self):
        """Test SmtpUsersListRequest with custom query params."""
        query_params = SmtpUsersListQueryParams(limit=50)
        request = SmtpUsersListRequest(domain_id="test-domain", query_params=query_params)
        
        assert request.domain_id == "test-domain"
        assert request.query_params.limit == 50
    
    def test_smtp_users_list_request_to_query_params(self):
        """Test SmtpUsersListRequest to_query_params delegation."""
        query_params = SmtpUsersListQueryParams(limit=40)
        request = SmtpUsersListRequest(domain_id="test-domain", query_params=query_params)
        result = request.to_query_params()
        
        assert result == {"limit": 40}
    
    def test_smtp_users_list_request_domain_id_validation(self):
        """Test domain_id validation."""
        with pytest.raises(ValidationError):
            SmtpUsersListRequest(domain_id="")
        
        with pytest.raises(ValidationError):
            SmtpUsersListRequest(domain_id="   ")
        
        # Test trimming
        request = SmtpUsersListRequest(domain_id="  test-domain  ")
        assert request.domain_id == "test-domain"


class TestSmtpUserGetRequest:
    """Test SmtpUserGetRequest model."""
    
    def test_basic_creation(self):
        """Test basic SmtpUserGetRequest creation."""
        request = SmtpUserGetRequest(domain_id="test-domain", smtp_user_id="user123")
        
        assert request.domain_id == "test-domain"
        assert request.smtp_user_id == "user123"
    
    def test_id_validation(self):
        """Test ID validation."""
        with pytest.raises(ValidationError):
            SmtpUserGetRequest(domain_id="", smtp_user_id="user123")
        
        with pytest.raises(ValidationError):
            SmtpUserGetRequest(domain_id="test-domain", smtp_user_id="")
        
        with pytest.raises(ValidationError):
            SmtpUserGetRequest(domain_id="   ", smtp_user_id="user123")
        
        with pytest.raises(ValidationError):
            SmtpUserGetRequest(domain_id="test-domain", smtp_user_id="   ")
    
    def test_id_trimming(self):
        """Test ID trimming."""
        request = SmtpUserGetRequest(domain_id="  test-domain  ", smtp_user_id="  user123  ")
        
        assert request.domain_id == "test-domain"
        assert request.smtp_user_id == "user123"


class TestSmtpUserCreateRequest:
    """Test SmtpUserCreateRequest model."""
    
    def test_basic_creation(self):
        """Test basic SmtpUserCreateRequest creation."""
        request = SmtpUserCreateRequest(domain_id="test-domain", name="Test User")
        
        assert request.domain_id == "test-domain"
        assert request.name == "Test User"
        assert request.enabled is None
    
    def test_creation_with_enabled(self):
        """Test SmtpUserCreateRequest creation with enabled flag."""
        request = SmtpUserCreateRequest(domain_id="test-domain", name="Test User", enabled=True)
        
        assert request.domain_id == "test-domain"
        assert request.name == "Test User"
        assert request.enabled is True
    
    def test_name_validation(self):
        """Test name validation."""
        with pytest.raises(ValidationError):
            SmtpUserCreateRequest(domain_id="test-domain", name="")
        
        with pytest.raises(ValidationError):
            SmtpUserCreateRequest(domain_id="test-domain", name="   ")
        
        # Test max length
        with pytest.raises(ValidationError):
            SmtpUserCreateRequest(domain_id="test-domain", name="a" * 51)
        
        # Test valid max length
        request = SmtpUserCreateRequest(domain_id="test-domain", name="a" * 50)
        assert request.name == "a" * 50
    
    def test_name_trimming(self):
        """Test name trimming."""
        request = SmtpUserCreateRequest(domain_id="test-domain", name="  Test User  ")
        assert request.name == "Test User"
    
    def test_domain_id_validation(self):
        """Test domain_id validation."""
        with pytest.raises(ValidationError):
            SmtpUserCreateRequest(domain_id="", name="Test User")
        
        with pytest.raises(ValidationError):
            SmtpUserCreateRequest(domain_id="   ", name="Test User")
        
        # Test trimming
        request = SmtpUserCreateRequest(domain_id="  test-domain  ", name="Test User")
        assert request.domain_id == "test-domain"
    
    def test_to_json(self):
        """Test to_json method."""
        request = SmtpUserCreateRequest(domain_id="test-domain", name="Test User")
        result = request.to_json()
        
        assert result == {"name": "Test User"}
    
    def test_to_json_with_enabled(self):
        """Test to_json method with enabled flag."""
        request = SmtpUserCreateRequest(domain_id="test-domain", name="Test User", enabled=False)
        result = request.to_json()
        
        assert result == {"name": "Test User", "enabled": False}


class TestSmtpUserUpdateRequest:
    """Test SmtpUserUpdateRequest model."""
    
    def test_basic_creation(self):
        """Test basic SmtpUserUpdateRequest creation."""
        request = SmtpUserUpdateRequest(
            domain_id="test-domain", 
            smtp_user_id="user123", 
            name="Updated User"
        )
        
        assert request.domain_id == "test-domain"
        assert request.smtp_user_id == "user123"
        assert request.name == "Updated User"
        assert request.enabled is None
    
    def test_creation_with_enabled(self):
        """Test SmtpUserUpdateRequest creation with enabled flag."""
        request = SmtpUserUpdateRequest(
            domain_id="test-domain", 
            smtp_user_id="user123", 
            name="Updated User", 
            enabled=True
        )
        
        assert request.domain_id == "test-domain"
        assert request.smtp_user_id == "user123"
        assert request.name == "Updated User"
        assert request.enabled is True
    
    def test_id_validation(self):
        """Test ID validation."""
        with pytest.raises(ValidationError):
            SmtpUserUpdateRequest(domain_id="", smtp_user_id="user123", name="Test")
        
        with pytest.raises(ValidationError):
            SmtpUserUpdateRequest(domain_id="test-domain", smtp_user_id="", name="Test")
    
    def test_name_validation(self):
        """Test name validation."""
        with pytest.raises(ValidationError):
            SmtpUserUpdateRequest(domain_id="test-domain", smtp_user_id="user123", name="")
        
        with pytest.raises(ValidationError):
            SmtpUserUpdateRequest(domain_id="test-domain", smtp_user_id="user123", name="   ")
        
        # Test max length
        with pytest.raises(ValidationError):
            SmtpUserUpdateRequest(domain_id="test-domain", smtp_user_id="user123", name="a" * 51)
    
    def test_to_json(self):
        """Test to_json method."""
        request = SmtpUserUpdateRequest(
            domain_id="test-domain", 
            smtp_user_id="user123", 
            name="Updated User"
        )
        result = request.to_json()
        
        assert result == {"name": "Updated User"}
    
    def test_to_json_with_enabled(self):
        """Test to_json method with enabled flag."""
        request = SmtpUserUpdateRequest(
            domain_id="test-domain", 
            smtp_user_id="user123", 
            name="Updated User", 
            enabled=False
        )
        result = request.to_json()
        
        assert result == {"name": "Updated User", "enabled": False}


class TestSmtpUserDeleteRequest:
    """Test SmtpUserDeleteRequest model."""
    
    def test_basic_creation(self):
        """Test basic SmtpUserDeleteRequest creation."""
        request = SmtpUserDeleteRequest(domain_id="test-domain", smtp_user_id="user123")
        
        assert request.domain_id == "test-domain"
        assert request.smtp_user_id == "user123"
    
    def test_id_validation(self):
        """Test ID validation."""
        with pytest.raises(ValidationError):
            SmtpUserDeleteRequest(domain_id="", smtp_user_id="user123")
        
        with pytest.raises(ValidationError):
            SmtpUserDeleteRequest(domain_id="test-domain", smtp_user_id="")


class TestSmtpUser:
    """Test SmtpUser model."""
    
    def test_basic_creation(self):
        """Test basic SmtpUser creation."""
        user = SmtpUser(
            id="user123",
            name="Test User",
            username="MS_test@example.com",
            password="password123",
            enabled=True,
            accessed_at=None,
            server="127.0.0.1",
            port=465,
            domain_id="domain123"
        )
        
        assert user.id == "user123"
        assert user.name == "Test User"
        assert user.username == "MS_test@example.com"
        assert user.password == "password123"
        assert user.enabled is True
        assert user.accessed_at is None
        assert user.server == "127.0.0.1"
        assert user.port == 465
        assert user.domain_id == "domain123"
    
    def test_creation_with_accessed_at(self):
        """Test SmtpUser creation with accessed_at datetime."""
        now = datetime.now()
        user = SmtpUser(
            id="user123",
            name="Test User",
            username="MS_test@example.com",
            password="password123",
            enabled=True,
            accessed_at=now,
            server="127.0.0.1",
            port=465,
            domain_id="domain123"
        )
        
        assert user.accessed_at == now


class TestResponseModels:
    """Test response models."""
    
    def test_smtp_users_list_response(self):
        """Test SmtpUsersListResponse model."""
        user = SmtpUser(
            id="user123",
            name="Test User",
            username="MS_test@example.com",
            password="password123",
            enabled=True,
            accessed_at=None,
            server="127.0.0.1",
            port=465,
            domain_id="domain123"
        )
        
        response = SmtpUsersListResponse(data=[user])
        
        assert len(response.data) == 1
        assert response.data[0].id == "user123"
    
    def test_smtp_user_response(self):
        """Test SmtpUserResponse model."""
        user = SmtpUser(
            id="user123",
            name="Test User",
            username="MS_test@example.com",
            password="password123",
            enabled=True,
            accessed_at=None,
            server="127.0.0.1",
            port=465,
            domain_id="domain123"
        )
        
        response = SmtpUserResponse(data=user)
        
        assert response.data.id == "user123"
    
    def test_smtp_user_create_response(self):
        """Test SmtpUserCreateResponse model."""
        user = SmtpUser(
            id="user123",
            name="Test User",
            username="MS_test@example.com",
            password="password123",
            enabled=True,
            accessed_at=None,
            server="127.0.0.1",
            port=465,
            domain_id="domain123"
        )
        
        response = SmtpUserCreateResponse(data=user)
        
        assert response.data.id == "user123" 