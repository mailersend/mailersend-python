import pytest
from tests.test_helpers import vcr, email_client
import os

from mailersend.models.identities import (
    IdentityListRequest,
    IdentityCreateRequest,
    IdentityGetRequest,
    IdentityGetByEmailRequest,
    IdentityUpdateRequest,
    IdentityUpdateByEmailRequest,
    IdentityDeleteRequest,
    IdentityDeleteByEmailRequest,
    IdentityListQueryParams,
)
from mailersend.models.base import APIResponse


@pytest.fixture
def basic_identity_list_request():
    """Basic identity list request"""
    return IdentityListRequest(
        query_params=IdentityListQueryParams(page=1, limit=10)
    )


@pytest.fixture
def identity_get_request():
    """Identity get request with test identity ID"""
    return IdentityGetRequest(identity_id="test-identity-id")


@pytest.fixture
def sample_identity_data():
    """Sample identity data for testing"""
    return {
        "domain_id": os.environ.get("SDK_DOMAIN_ID", "test-domain-id"),
        "name": "Test Identity",
        "email": os.environ.get("SDK_FROM_EMAIL", "test@example.com"),
        "reply_to_email": os.environ.get("SDK_FROM_EMAIL", "reply@example.com"),
        "reply_to_name": "Reply Test",
        "add_note": True,
        "personal_note": "Test identity for integration testing"
    }


class TestIdentitiesIntegration:
    @vcr.use_cassette("identities_create_not_available.yaml")
    def test_create_identity_endpoint_not_available(self, email_client, sample_identity_data):
        from mailersend.exceptions import BadRequestError
        
        request = IdentityCreateRequest(
            domain_id=sample_identity_data["domain_id"],
            name=sample_identity_data["name"],
            email=sample_identity_data["email"],
            reply_to_email=sample_identity_data["reply_to_email"],
            reply_to_name=sample_identity_data["reply_to_name"],
            add_note=sample_identity_data["add_note"],
            personal_note=sample_identity_data["personal_note"]
        )

        with pytest.raises(BadRequestError) as exc_info:
            email_client.identities.create_identity(request)

        error_str = str(exc_info.value).lower()
        assert "the email has already been taken." in error_str

    @vcr.use_cassette("identities_get_single.yaml")
    def test_get_identity_endpoint_not_available(self, email_client, identity_get_request):
        from mailersend.exceptions import ResourceNotFoundError
        
        with pytest.raises(ResourceNotFoundError) as exc_info:
            email_client.identities.get_identity(identity_get_request)

        error_str = str(exc_info.value).lower()
        assert "could not be found" in error_str or "not found" in error_str

    @vcr.use_cassette("identities_get_by_email.yaml")
    def test_get_identity_by_email_endpoint_not_available(self, email_client):
        """Test that get identity by email endpoint is not available."""
        from mailersend.exceptions import ResourceNotFoundError
        
        request = IdentityGetByEmailRequest(email="test@example.com")

        with pytest.raises(ResourceNotFoundError) as exc_info:
            email_client.identities.get_identity_by_email(request)

        error_str = str(exc_info.value).lower()
        assert "could not be found" in error_str or "not found" in error_str

    @vcr.use_cassette("identities_update_by_id.yaml")
    def test_update_identity_endpoint_not_available(self, email_client):
        """Test that update identity endpoint is not available."""
        from mailersend.exceptions import ResourceNotFoundError
        
        request = IdentityUpdateRequest(
            identity_id="test-identity-id",
            name="Updated Test Identity"
        )

        with pytest.raises(ResourceNotFoundError) as exc_info:
            email_client.identities.update_identity(request)

        error_str = str(exc_info.value).lower()
        assert "could not be found" in error_str or "not found" in error_str

    @vcr.use_cassette("identities_update_by_email.yaml")
    def test_update_identity_by_email_endpoint_not_available(self, email_client):
        """Test that update identity by email endpoint is not available."""
        from mailersend.exceptions import ResourceNotFoundError
        
        request = IdentityUpdateByEmailRequest(
            email="test@example.com",
            name="Updated Test Identity"
        )

        with pytest.raises(ResourceNotFoundError) as exc_info:
            email_client.identities.update_identity_by_email(request)

        error_str = str(exc_info.value).lower()
        assert "could not be found" in error_str or "not found" in error_str

    @vcr.use_cassette("identities_delete_by_id.yaml")
    def test_delete_identity_endpoint_not_available(self, email_client, identity_get_request):
        """Test that delete identity endpoint is not available."""
        from mailersend.exceptions import ResourceNotFoundError
        
        delete_request = IdentityDeleteRequest(
            identity_id=identity_get_request.identity_id
        )

        with pytest.raises(ResourceNotFoundError) as exc_info:
            email_client.identities.delete_identity(delete_request)

        error_str = str(exc_info.value).lower()
        assert "could not be found" in error_str or "not found" in error_str

    @vcr.use_cassette("identities_delete_by_email.yaml")
    def test_delete_identity_by_email_endpoint_not_available(self, email_client):
        """Test that delete identity by email endpoint is not available."""
        from mailersend.exceptions import ResourceNotFoundError
        
        request = IdentityDeleteByEmailRequest(email="test@example.com")

        with pytest.raises(ResourceNotFoundError) as exc_info:
            email_client.identities.delete_identity_by_email(request)

        error_str = str(exc_info.value).lower()
        assert "could not be found" in error_str or "not found" in error_str

    @vcr.use_cassette("identities_validation_error.yaml")
    def test_list_identities_validation_error(self, email_client):
        """Test that invalid request raises validation error."""
        with pytest.raises(Exception) as exc_info:
            # Pass invalid request type
            email_client.identities.list_identities("invalid-request")

        # Should raise an AttributeError for invalid request type
        error_str = str(exc_info.value).lower()
        assert (
            "attribute" in error_str
            or "to_query_params" in error_str
        )

    def test_create_identity_model_validation(self):
        """Test model validation for identity creation."""
        # Test empty domain_id
        with pytest.raises(ValueError) as exc_info:
            IdentityCreateRequest(
                domain_id="",
                name="Test",
                email="test@example.com"
            )
        assert "domain id is required" in str(exc_info.value).lower()

        # Test empty name
        with pytest.raises(ValueError) as exc_info:
            IdentityCreateRequest(
                domain_id="test-domain",
                name="",
                email="test@example.com"
            )
        assert "name is required" in str(exc_info.value).lower()

        # Test empty email
        with pytest.raises(ValueError) as exc_info:
            IdentityCreateRequest(
                domain_id="test-domain",
                name="Test",
                email=""
            )
        assert "email is required" in str(exc_info.value).lower()

        # Test invalid email format
        with pytest.raises(ValueError) as exc_info:
            IdentityCreateRequest(
                domain_id="test-domain",
                name="Test",
                email="invalid-email"
            )
        assert "invalid email format" in str(exc_info.value).lower()

    def test_identity_list_query_params_validation(self):
        """Test validation for identity list query parameters."""
        # Test valid parameters
        params = IdentityListQueryParams(page=1, limit=25, domain_id="test-domain")
        assert params.page == 1
        assert params.limit == 25
        assert params.domain_id == "test-domain"
        
        # Test minimum limit validation
        with pytest.raises(ValueError):
            IdentityListQueryParams(limit=5)  # Below minimum of 10
            
        # Test maximum limit validation  
        with pytest.raises(ValueError):
            IdentityListQueryParams(limit=150)  # Above maximum of 100
            
        # Test minimum page validation
        with pytest.raises(ValueError):
            IdentityListQueryParams(page=0)  # Below minimum of 1

    def test_identity_update_request_validation(self):
        """Test validation for identity update requests."""
        # Test empty identity_id
        with pytest.raises(ValueError) as exc_info:
            IdentityUpdateRequest(identity_id="", name="Test")
        assert "identity id is required" in str(exc_info.value).lower()
        
        # Test empty email for email-based updates
        with pytest.raises(ValueError) as exc_info:
            IdentityUpdateByEmailRequest(email="", name="Test")
        assert "email is required" in str(exc_info.value).lower()
        
        # Test invalid email format for email-based updates
        with pytest.raises(ValueError) as exc_info:
            IdentityUpdateByEmailRequest(email="invalid-email", name="Test")
        assert "invalid email format" in str(exc_info.value).lower() 