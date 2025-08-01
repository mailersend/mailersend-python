import pytest
from tests.test_helpers import vcr, email_client
import os

from mailersend.models.smtp_users import (
    SmtpUsersListRequest,
    SmtpUserGetRequest,
    SmtpUserCreateRequest,
    SmtpUserUpdateRequest,
    SmtpUserDeleteRequest,
    SmtpUsersListQueryParams,
)
from mailersend.models.base import APIResponse
from mailersend.builders.smtp_users import SmtpUsersBuilder


@pytest.fixture
def test_domain_id():
    """Get the test domain ID from environment variables"""
    return os.environ.get("SDK_DOMAIN_ID", "test-domain-id")


@pytest.fixture
def basic_smtp_users_list_request(test_domain_id):
    """Basic SMTP users list request"""
    return SmtpUsersListRequest(
        domain_id=test_domain_id,
        query_params=SmtpUsersListQueryParams(limit=10)
    )


@pytest.fixture
def smtp_user_get_request(test_domain_id):
    """SMTP user get request with test SMTP user ID"""
    return SmtpUserGetRequest(
        domain_id=test_domain_id,
        smtp_user_id="test-smtp-user-id"
    )


@pytest.fixture
def sample_smtp_user_data(test_domain_id):
    """Sample SMTP user data for testing"""
    return {
        "domain_id": test_domain_id,
        "name": "Test SMTP User",
        "enabled": True
    }


class TestSmtpUsersIntegration:
    """Integration tests for SMTP Users API."""

    @vcr.use_cassette("smtp_users_list_basic.yaml")
    def test_list_smtp_users_basic(self, email_client, basic_smtp_users_list_request):
        """Test listing SMTP users with basic parameters."""
        response = email_client.smtp_users.list_smtp_users(basic_smtp_users_list_request)

        assert isinstance(response, APIResponse)
        assert response.status_code == 200
        assert response.data is not None

        # Check that we have the expected structure
        if "data" in response.data:
            smtp_users = response.data["data"]
            assert isinstance(smtp_users, list)

            # If we have SMTP users, check the structure
            if smtp_users:
                first_user = smtp_users[0]
                assert "id" in first_user
                assert "name" in first_user
                assert "enabled" in first_user
                assert "created_at" in first_user

    @vcr.use_cassette("smtp_users_list_with_limit.yaml")
    def test_list_smtp_users_with_limit(self, email_client, test_domain_id):
        """Test listing SMTP users with custom limit."""
        request = SmtpUsersListRequest(
            domain_id=test_domain_id,
            query_params=SmtpUsersListQueryParams(limit=25)
        )

        response = email_client.smtp_users.list_smtp_users(request)

        assert isinstance(response, APIResponse)
        assert response.status_code == 200

        # Check that the limit was applied
        if "meta" in response.data:
            meta = response.data["meta"]
            # API may return different structure for meta
            if "per_page" in meta:
                assert meta["per_page"] == 25

    @vcr.use_cassette("smtp_users_list_invalid_domain.yaml")
    def test_list_smtp_users_invalid_domain(self, email_client):
        """Test listing SMTP users with invalid domain ID returns 404."""
        from mailersend.exceptions import ResourceNotFoundError
        
        request = SmtpUsersListRequest(
            domain_id="invalid-domain-id",
            query_params=SmtpUsersListQueryParams(limit=10)
        )

        with pytest.raises(ResourceNotFoundError) as exc_info:
            email_client.smtp_users.list_smtp_users(request)

        assert "not found" in str(exc_info.value).lower() or "404" in str(exc_info.value) or "could not be found" in str(exc_info.value).lower()

    @vcr.use_cassette("smtp_users_get_not_found.yaml")
    def test_get_smtp_user_not_found(self, email_client, smtp_user_get_request):
        """Test getting a non-existent SMTP user returns 404."""
        from mailersend.exceptions import ResourceNotFoundError
        
        with pytest.raises(ResourceNotFoundError) as exc_info:
            email_client.smtp_users.get_smtp_user(smtp_user_get_request)

        assert "not found" in str(exc_info.value).lower() or "404" in str(exc_info.value) or "could not be found" in str(exc_info.value).lower()

    @vcr.use_cassette("smtp_users_create_invalid_domain.yaml")
    def test_create_smtp_user_invalid_domain(self, email_client, sample_smtp_user_data):
        """Test creating SMTP user with invalid domain ID returns 404."""
        from mailersend.exceptions import ResourceNotFoundError
        
        request = SmtpUserCreateRequest(
            domain_id="invalid-domain-id",
            name=sample_smtp_user_data["name"],
            enabled=sample_smtp_user_data["enabled"]
        )

        with pytest.raises(ResourceNotFoundError) as exc_info:
            email_client.smtp_users.create_smtp_user(request)

        assert "not found" in str(exc_info.value).lower() or "404" in str(exc_info.value) or "could not be found" in str(exc_info.value).lower()

    @vcr.use_cassette("smtp_users_update_not_found.yaml")
    def test_update_smtp_user_not_found(self, email_client, test_domain_id):
        """Test updating non-existent SMTP user returns 404."""
        from mailersend.exceptions import ResourceNotFoundError
        
        request = SmtpUserUpdateRequest(
            domain_id=test_domain_id,
            smtp_user_id="test-smtp-user-id",
            name="Updated SMTP User",
            enabled=False
        )

        with pytest.raises(ResourceNotFoundError) as exc_info:
            email_client.smtp_users.update_smtp_user(request)

        assert "not found" in str(exc_info.value).lower() or "404" in str(exc_info.value) or "could not be found" in str(exc_info.value).lower()

    @vcr.use_cassette("smtp_users_delete_not_found.yaml")
    def test_delete_smtp_user_not_found(self, email_client, smtp_user_get_request):
        """Test deleting non-existent SMTP user returns 404."""
        from mailersend.exceptions import ResourceNotFoundError
        
        delete_request = SmtpUserDeleteRequest(
            domain_id=smtp_user_get_request.domain_id,
            smtp_user_id=smtp_user_get_request.smtp_user_id
        )

        with pytest.raises(ResourceNotFoundError) as exc_info:
            email_client.smtp_users.delete_smtp_user(delete_request)

        assert "not found" in str(exc_info.value).lower() or "404" in str(exc_info.value) or "could not be found" in str(exc_info.value).lower()

    @vcr.use_cassette("smtp_users_validation_error.yaml")
    def test_list_smtp_users_validation_error(self, email_client):
        """Test that invalid request raises validation error."""
        with pytest.raises(Exception) as exc_info:
            # Pass invalid request type
            email_client.smtp_users.list_smtp_users("invalid-request")

        # Should raise an AttributeError for invalid request type
        error_str = str(exc_info.value).lower()
        assert (
            "attribute" in error_str
            or "to_query_params" in error_str
        )

    @vcr.use_cassette("smtp_users_api_response_structure.yaml")
    def test_api_response_structure(self, email_client, basic_smtp_users_list_request):
        """Test that API response has the expected structure and metadata."""
        response = email_client.smtp_users.list_smtp_users(basic_smtp_users_list_request)

        assert isinstance(response, APIResponse)
        assert response.status_code == 200
        assert hasattr(response, "data")
        assert hasattr(response, "headers")

        # Check for rate limiting headers
        if response.rate_limit_remaining is not None:
            assert isinstance(response.rate_limit_remaining, int)
            # Rate limit remaining can be -1 for unlimited plans
        assert response.rate_limit_remaining is not None

        # Check for request ID
        if response.request_id is not None:
            assert isinstance(response.request_id, str)
            assert len(response.request_id) > 0

    @vcr.use_cassette("smtp_users_empty_result.yaml")
    def test_list_smtp_users_empty_result(self, email_client, basic_smtp_users_list_request):
        """Test listing SMTP users when no users exist."""
        response = email_client.smtp_users.list_smtp_users(basic_smtp_users_list_request)

        assert isinstance(response, APIResponse)
        assert response.status_code == 200
        assert response.data is not None

        # Should have data array (may not be empty due to previous tests creating data)
        if "data" in response.data:
            assert isinstance(response.data["data"], list)

    def test_smtp_user_create_model_validation(self):
        """Test model validation for SMTP user creation."""
        # Test empty domain_id - this will raise a pydantic ValidationError first
        from pydantic import ValidationError
        with pytest.raises(ValidationError) as exc_info:
            SmtpUserCreateRequest(
                domain_id="",
                name="Test User"
            )
        assert "string should have at least 1 character" in str(exc_info.value).lower()

        # Test empty name - this will also raise a pydantic ValidationError first
        with pytest.raises(ValidationError) as exc_info:
            SmtpUserCreateRequest(
                domain_id="test-domain",
                name=""
            )
        assert "string should have at least 1 character" in str(exc_info.value).lower()

        # Test name too long - this will also raise a pydantic ValidationError first
        with pytest.raises(ValidationError) as exc_info:
            SmtpUserCreateRequest(
                domain_id="test-domain",
                name="x" * 51  # Exceeds 50 character limit
            )
        assert "string should have at most 50 characters" in str(exc_info.value).lower()

    def test_smtp_user_get_model_validation(self):
        """Test model validation for SMTP user retrieval."""
        # Test empty domain_id - this will raise a pydantic ValidationError first
        from pydantic import ValidationError
        with pytest.raises(ValidationError) as exc_info:
            SmtpUserGetRequest(
                domain_id="",
                smtp_user_id="test-id"
            )
        assert "string should have at least 1 character" in str(exc_info.value).lower()

        # Test empty smtp_user_id - this will also raise a pydantic ValidationError first
        with pytest.raises(ValidationError) as exc_info:
            SmtpUserGetRequest(
                domain_id="test-domain",
                smtp_user_id=""
            )
        assert "string should have at least 1 character" in str(exc_info.value).lower()

    def test_smtp_users_list_query_params_validation(self):
        """Test validation for SMTP users list query parameters."""
        # Test valid parameters
        params = SmtpUsersListQueryParams(limit=25)
        assert params.limit == 25
        
        # Test minimum limit validation
        with pytest.raises(ValueError):
            SmtpUsersListQueryParams(limit=5)  # Below minimum of 10
            
        # Test maximum limit validation  
        with pytest.raises(ValueError):
            SmtpUsersListQueryParams(limit=150)  # Above maximum of 100


class TestSmtpUsersBuilderIntegration:
    """Integration tests for SmtpUsersBuilder API."""

    @vcr.use_cassette("smtp_users_builder_list_basic.yaml")
    def test_builder_list_basic_usage(self, email_client, test_domain_id):
        """Test basic SMTP users list using builder."""
        builder = SmtpUsersBuilder()
        request = builder.domain_id(test_domain_id).limit(10).build_smtp_users_list()
        
        response = email_client.smtp_users.list_smtp_users(request)
        
        assert isinstance(response, APIResponse)
        assert response.status_code == 200

    @vcr.use_cassette("smtp_users_builder_list_with_custom_limit.yaml")
    def test_builder_list_with_custom_limit(self, email_client, test_domain_id):
        """Test SMTP users list with custom limit using builder."""
        builder = SmtpUsersBuilder()
        request = builder.domain_id(test_domain_id).limit(50).build_smtp_users_list()
        
        response = email_client.smtp_users.list_smtp_users(request)
        
        assert isinstance(response, APIResponse)
        assert response.status_code == 200

    @vcr.use_cassette("smtp_users_builder_get_not_found.yaml")
    def test_builder_get_not_found(self, email_client, test_domain_id):
        """Test getting non-existent SMTP user using builder."""
        from mailersend.exceptions import ResourceNotFoundError
        
        builder = SmtpUsersBuilder()
        request = builder.domain_id(test_domain_id).smtp_user_id("test-smtp-user-id").build_smtp_user_get()
        
        with pytest.raises(ResourceNotFoundError):
            email_client.smtp_users.get_smtp_user(request)

    @vcr.use_cassette("smtp_users_builder_create_invalid_domain.yaml")
    def test_builder_create_invalid_domain(self, email_client):
        """Test creating SMTP user with invalid domain using builder."""
        from mailersend.exceptions import ResourceNotFoundError
        
        builder = SmtpUsersBuilder()
        request = (builder
            .domain_id("invalid-domain-id")
            .name("Test User")
            .enabled(True)
            .build_smtp_user_create())
        
        with pytest.raises(ResourceNotFoundError):
            email_client.smtp_users.create_smtp_user(request)

    @vcr.use_cassette("smtp_users_builder_update_not_found.yaml")
    def test_builder_update_not_found(self, email_client, test_domain_id):
        """Test updating non-existent SMTP user using builder."""
        from mailersend.exceptions import ResourceNotFoundError
        
        builder = SmtpUsersBuilder()
        request = (builder
            .domain_id(test_domain_id)
            .smtp_user_id("test-smtp-user-id")
            .name("Updated User")
            .enabled(False)
            .build_smtp_user_update())
        
        with pytest.raises(ResourceNotFoundError):
            email_client.smtp_users.update_smtp_user(request)

    @vcr.use_cassette("smtp_users_builder_delete_not_found.yaml")
    def test_builder_delete_not_found(self, email_client, test_domain_id):
        """Test deleting non-existent SMTP user using builder."""
        from mailersend.exceptions import ResourceNotFoundError
        
        builder = SmtpUsersBuilder()
        request = (builder
            .domain_id(test_domain_id)
            .smtp_user_id("test-smtp-user-id")
            .build_smtp_user_delete())
        
        with pytest.raises(ResourceNotFoundError):
            email_client.smtp_users.delete_smtp_user(request)

    def test_builder_fluent_interface(self):
        """Test that builder methods return self for chaining."""
        builder = SmtpUsersBuilder()
        
        # Test method chaining
        result = (builder
            .domain_id("test-domain")
            .smtp_user_id("test-user")
            .name("Test User")
            .enabled(True)
            .limit(10))
        
        assert result is builder
        
        # Verify the builder state
        list_request = builder.build_smtp_users_list()
        assert list_request.domain_id == "test-domain"
        assert list_request.query_params.limit == 10
        
        get_request = builder.build_smtp_user_get()
        assert get_request.domain_id == "test-domain"
        assert get_request.smtp_user_id == "test-user"
        
        create_request = builder.build_smtp_user_create()
        assert create_request.domain_id == "test-domain"
        assert create_request.name == "Test User"
        assert create_request.enabled is True

    def test_builder_validation_errors(self):
        """Test builder validation for invalid inputs."""
        from mailersend.exceptions import ValidationError
        
        builder = SmtpUsersBuilder()
        
        # Test invalid limit (too low)
        with pytest.raises(ValidationError) as exc_info:
            builder.limit(5)
        assert "limit must be between 10 and 100" in str(exc_info.value).lower()
        
        # Test invalid limit (too high)
        with pytest.raises(ValidationError) as exc_info:
            builder.limit(150)
        assert "limit must be between 10 and 100" in str(exc_info.value).lower()
        
        # Test invalid page
        with pytest.raises(ValidationError) as exc_info:
            builder.page(0)
        assert "page must be >= 1" in str(exc_info.value).lower()
        
        # Test building list request without domain_id
        fresh_builder = SmtpUsersBuilder()
        with pytest.raises(ValidationError) as exc_info:
            fresh_builder.build_smtp_users_list()
        assert "domain id is required" in str(exc_info.value).lower()
        
        # Test building get request without smtp_user_id
        with pytest.raises(ValidationError) as exc_info:
            fresh_builder.domain_id("test").build_smtp_user_get()
        assert "smtp user id is required" in str(exc_info.value).lower()
        
        # Test building create request without name
        with pytest.raises(ValidationError) as exc_info:
            fresh_builder.domain_id("test").build_smtp_user_create()
        assert "name is required" in str(exc_info.value).lower()

    def test_builder_default_values(self):
        """Test that builder uses appropriate default values."""
        builder = SmtpUsersBuilder()
        
        # Build request with minimal required fields
        request = builder.domain_id("test-domain").build_smtp_users_list()
        
        # Should use default values from the model
        assert request.query_params.limit == 25

    def test_builder_request_variations(self):
        """Test various request building scenarios with builder."""
        builder = SmtpUsersBuilder()
        
        # Test create request with enabled=True
        create_request1 = (builder
            .domain_id("test-domain")
            .name("Enabled User")
            .enabled(True)
            .build_smtp_user_create())
        assert create_request1.enabled is True
        
        # Test create request with enabled=False
        create_request2 = (builder
            .domain_id("test-domain")
            .name("Disabled User")
            .enabled(False)
            .build_smtp_user_create())
        assert create_request2.enabled is False
        
        # Test create request without enabled (should be None)
        builder_fresh = SmtpUsersBuilder()
        create_request3 = (builder_fresh
            .domain_id("test-domain")
            .name("Default User")
            .build_smtp_user_create())
        assert create_request3.enabled is None

    def test_builder_json_serialization(self):
        """Test that builder-created requests serialize correctly to JSON."""
        builder = SmtpUsersBuilder()
        
        # Test create request JSON
        create_request = (builder
            .domain_id("test-domain")
            .name("Test User")
            .enabled(True)
            .build_smtp_user_create())
        
        json_data = create_request.to_json()
        assert json_data["name"] == "Test User"
        assert json_data["enabled"] is True
        
        # Test create request JSON without enabled
        builder_fresh = SmtpUsersBuilder()
        create_request_no_enabled = (builder_fresh
            .domain_id("test-domain")
            .name("Test User")
            .build_smtp_user_create())
        
        json_data_no_enabled = create_request_no_enabled.to_json()
        assert json_data_no_enabled["name"] == "Test User"
        assert "enabled" not in json_data_no_enabled

    @vcr.use_cassette("smtp_users_comprehensive_workflow.yaml") 
    def test_comprehensive_smtp_users_workflow(self, email_client, test_domain_id):
        """Test comprehensive workflow covering list, CRUD operations, error scenarios, and builder usage."""
        # Test list with different configurations
        list_request = SmtpUsersListRequest(
            domain_id=test_domain_id,
            query_params=SmtpUsersListQueryParams(limit=10)
        )
        
        response = email_client.smtp_users.list_smtp_users(list_request)
        assert isinstance(response, APIResponse)
        assert response.status_code == 200
        
        # Test builder pattern with different configurations
        builder = SmtpUsersBuilder()
        
        # Test list with builder
        builder_request = builder.domain_id(test_domain_id).limit(25).build_smtp_users_list()
        builder_response = email_client.smtp_users.list_smtp_users(builder_request)
        assert isinstance(builder_response, APIResponse)
        assert builder_response.status_code == 200
        
        # Test error scenarios
        from mailersend.exceptions import ResourceNotFoundError
        
        # Test get non-existent user
        get_request = SmtpUserGetRequest(
            domain_id=test_domain_id,
            smtp_user_id="non-existent-id"
        )
        with pytest.raises(ResourceNotFoundError):
            email_client.smtp_users.get_smtp_user(get_request)
        
        # Test create with invalid domain
        create_request = SmtpUserCreateRequest(
            domain_id="invalid-domain",
            name="Test User"
        )
        with pytest.raises(ResourceNotFoundError):
            email_client.smtp_users.create_smtp_user(create_request)
        
        # Test builder error scenarios
        builder_get_request = builder.smtp_user_id("another-non-existent-id").build_smtp_user_get()
        with pytest.raises(ResourceNotFoundError):
            email_client.smtp_users.get_smtp_user(builder_get_request)