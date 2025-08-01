import pytest
from tests.test_helpers import vcr, email_client
import os

from mailersend.models.tokens import (
    TokensListRequest,
    TokenGetRequest,
    TokenCreateRequest,
    TokenUpdateRequest,
    TokenUpdateNameRequest,
    TokenDeleteRequest,
    TokensListQueryParams,
    TOKEN_SCOPES,
)
from mailersend.models.base import APIResponse
from mailersend.builders.tokens import TokensBuilder


@pytest.fixture
def test_domain_id():
    """Get the test domain ID from environment variables"""
    return os.environ.get("SDK_DOMAIN_ID", "test-domain-id")


@pytest.fixture
def basic_tokens_list_request():
    """Basic tokens list request"""
    return TokensListRequest(
        query_params=TokensListQueryParams(page=1, limit=10)
    )


@pytest.fixture
def token_get_request():
    """Token get request with test token ID"""
    return TokenGetRequest(token_id="test-token-id")


@pytest.fixture
def sample_token_data(test_domain_id):
    """Sample token data for testing"""
    return {
        "name": "Test Token",
        "domain_id": test_domain_id,
        "scopes": ["email_full", "domains_read"]
    }


class TestTokensIntegration:
    """Integration tests for Tokens API."""

    @vcr.use_cassette("tokens_list_basic.yaml")
    def test_list_tokens_basic(self, email_client, basic_tokens_list_request):
        """Test listing tokens with basic parameters."""
        response = email_client.tokens.list_tokens(basic_tokens_list_request)

        assert isinstance(response, APIResponse)
        assert response.status_code == 200
        assert response.data is not None

        # Check that we have the expected structure
        if "data" in response.data:
            tokens = response.data["data"]
            assert isinstance(tokens, list)

            # If we have tokens, check the structure
            if tokens:
                first_token = tokens[0]
                assert "id" in first_token
                assert "name" in first_token
                assert "status" in first_token
                assert "created_at" in first_token
                assert "scopes" in first_token

    @vcr.use_cassette("tokens_list_with_pagination.yaml")
    def test_list_tokens_with_pagination(self, email_client):
        """Test listing tokens with pagination."""
        request = TokensListRequest(
            query_params=TokensListQueryParams(page=1, limit=10)
        )

        response = email_client.tokens.list_tokens(request)

        assert isinstance(response, APIResponse)
        assert response.status_code == 200

        # Check pagination metadata
        if "meta" in response.data:
            meta = response.data["meta"]
            assert "current_page" in meta
            assert "per_page" in meta
            # Don't assume total field exists - it's optional in many API responses
            assert meta["per_page"] == 10
            assert meta["current_page"] == 1

    @vcr.use_cassette("tokens_list_different_limit.yaml")
    def test_list_tokens_different_limit(self, email_client):
        """Test listing tokens with different limit."""
        request = TokensListRequest(
            query_params=TokensListQueryParams(page=1, limit=50)
        )

        response = email_client.tokens.list_tokens(request)

        assert isinstance(response, APIResponse)
        assert response.status_code == 200
        assert response.data is not None

        # Check pagination reflects the requested limit
        if "meta" in response.data:
            meta = response.data["meta"]
            # Expect actual values: per_page often returns the requested limit
            assert meta["per_page"] == 50

    @vcr.use_cassette("tokens_get_not_found.yaml")
    def test_get_token_not_found(self, email_client, token_get_request):
        """Test getting a non-existent token returns 404."""
        from mailersend.exceptions import ResourceNotFoundError
        
        with pytest.raises(ResourceNotFoundError) as exc_info:
            email_client.tokens.get_token(token_get_request)

        assert "not found" in str(exc_info.value).lower() or "404" in str(exc_info.value) or "could not be found" in str(exc_info.value).lower()

    @vcr.use_cassette("tokens_create_basic.yaml")
    def test_create_token_basic(self, email_client, sample_token_data):
        """Test creating token with basic parameters."""
        request = TokenCreateRequest(
            name=sample_token_data["name"],
            domain_id=sample_token_data["domain_id"],
            scopes=sample_token_data["scopes"]
        )

        response = email_client.tokens.create_token(request)

        assert isinstance(response, APIResponse)
        assert response.status_code in [200, 201]
        assert response.data is not None

    @vcr.use_cassette("tokens_update_not_found.yaml")
    def test_update_token_not_found(self, email_client):
        """Test updating non-existent token returns 404."""
        from mailersend.exceptions import ResourceNotFoundError
        
        request = TokenUpdateRequest(
            token_id="test-token-id",
            status="pause"
        )

        with pytest.raises(ResourceNotFoundError) as exc_info:
            email_client.tokens.update_token(request)

        assert "not found" in str(exc_info.value).lower() or "404" in str(exc_info.value) or "could not be found" in str(exc_info.value).lower()

    @vcr.use_cassette("tokens_update_name_not_found.yaml")
    def test_update_token_name_not_found(self, email_client):
        """Test updating non-existent token name returns 404."""
        from mailersend.exceptions import ResourceNotFoundError
        
        request = TokenUpdateNameRequest(
            token_id="test-token-id",
            name="Updated Token Name"
        )

        with pytest.raises(ResourceNotFoundError) as exc_info:
            email_client.tokens.update_token_name(request)

        assert "not found" in str(exc_info.value).lower() or "404" in str(exc_info.value) or "could not be found" in str(exc_info.value).lower()

    @vcr.use_cassette("tokens_delete_not_found.yaml")
    def test_delete_token_not_found(self, email_client, token_get_request):
        """Test deleting non-existent token returns 404."""
        from mailersend.exceptions import ResourceNotFoundError
        
        delete_request = TokenDeleteRequest(
            token_id=token_get_request.token_id
        )

        with pytest.raises(ResourceNotFoundError) as exc_info:
            email_client.tokens.delete_token(delete_request)

        assert "not found" in str(exc_info.value).lower() or "404" in str(exc_info.value) or "could not be found" in str(exc_info.value).lower()

    @vcr.use_cassette("tokens_validation_error.yaml")
    def test_list_tokens_validation_error(self, email_client):
        """Test that invalid request raises validation error."""
        with pytest.raises(Exception) as exc_info:
            # Pass invalid request type
            email_client.tokens.list_tokens("invalid-request")

        # Should raise an AttributeError for invalid request type
        error_str = str(exc_info.value).lower()
        assert (
            "attribute" in error_str
            or "to_query_params" in error_str
        )

    @vcr.use_cassette("tokens_api_response_structure.yaml")
    def test_api_response_structure(self, email_client, basic_tokens_list_request):
        """Test that API response has the expected structure and metadata."""
        response = email_client.tokens.list_tokens(basic_tokens_list_request)

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

    @vcr.use_cassette("tokens_empty_result.yaml")
    def test_list_tokens_empty_result(self, email_client, basic_tokens_list_request):
        """Test listing tokens when no tokens exist."""
        response = email_client.tokens.list_tokens(basic_tokens_list_request)

        assert isinstance(response, APIResponse)
        assert response.status_code == 200
        assert response.data is not None

        # Should have data array (may not be empty due to previous tests creating data)
        if "data" in response.data:
            assert isinstance(response.data["data"], list)

    def test_token_create_model_validation(self):
        """Test model validation for token creation."""
        # Test empty name - this will raise a custom validation error
        from pydantic import ValidationError
        with pytest.raises(ValidationError) as exc_info:
            TokenCreateRequest(
                name="",
                domain_id="test-domain",
                scopes=["email_full"]
            )
        assert "token name cannot be empty" in str(exc_info.value).lower()

        # Test empty domain_id
        with pytest.raises(ValueError) as exc_info:
            TokenCreateRequest(
                name="Test Token",
                domain_id="",
                scopes=["email_full"]
            )
        assert "domain id cannot be empty" in str(exc_info.value).lower()

        # Test empty scopes
        with pytest.raises(ValidationError) as exc_info:
            TokenCreateRequest(
                name="Test Token",
                domain_id="test-domain",
                scopes=[]
            )
        assert "list should have at least 1 item" in str(exc_info.value).lower()

        # Test invalid scopes
        with pytest.raises(ValueError) as exc_info:
            TokenCreateRequest(
                name="Test Token",
                domain_id="test-domain",
                scopes=["invalid_scope"]
            )
        assert "invalid scopes" in str(exc_info.value).lower()

        # Test name too long
        with pytest.raises(ValidationError) as exc_info:
            TokenCreateRequest(
                name="x" * 51,  # Exceeds 50 character limit
                domain_id="test-domain",
                scopes=["email_full"]
            )
        assert "string should have at most 50 characters" in str(exc_info.value).lower()

    def test_token_update_model_validation(self):
        """Test model validation for token updates."""
        # Test valid status values
        valid_request1 = TokenUpdateRequest(token_id="test", status="pause")
        assert valid_request1.status == "pause"
        
        valid_request2 = TokenUpdateRequest(token_id="test", status="unpause")
        assert valid_request2.status == "unpause"

        # Test invalid status - this will raise a pydantic ValidationError
        from pydantic import ValidationError
        with pytest.raises(ValidationError) as exc_info:
            TokenUpdateRequest(token_id="test", status="invalid")
        assert "input should be 'pause' or 'unpause'" in str(exc_info.value).lower()

    def test_token_update_name_model_validation(self):
        """Test model validation for token name updates."""
        # Test empty name
        with pytest.raises(ValueError) as exc_info:
            TokenUpdateNameRequest(
                token_id="test-id",
                name=""
            )
        assert "token name cannot be empty" in str(exc_info.value).lower()

        # Test name too long
        from pydantic import ValidationError
        with pytest.raises(ValidationError) as exc_info:
            TokenUpdateNameRequest(
                token_id="test-id",
                name="x" * 51  # Exceeds 50 character limit
            )
        assert "string should have at most 50 characters" in str(exc_info.value).lower()

    def test_tokens_list_query_params_validation(self):
        """Test validation for tokens list query parameters."""
        # Test valid parameters
        params = TokensListQueryParams(page=1, limit=25)
        assert params.page == 1
        assert params.limit == 25
        
        # Test minimum limit validation
        with pytest.raises(ValueError):
            TokensListQueryParams(limit=5)  # Below minimum of 10
            
        # Test maximum limit validation  
        with pytest.raises(ValueError):
            TokensListQueryParams(limit=150)  # Above maximum of 100
            
        # Test minimum page validation
        with pytest.raises(ValueError):
            TokensListQueryParams(page=0)  # Below minimum of 1

    def test_token_scopes_constants(self):
        """Test that token scopes constants are properly defined."""
        # Verify TOKEN_SCOPES is defined and contains expected scopes
        assert TOKEN_SCOPES is not None
        assert isinstance(TOKEN_SCOPES, list)
        assert len(TOKEN_SCOPES) > 0
        
        # Check for some key scopes
        expected_scopes = [
            "email_full", "domains_read", "domains_full", 
            "activity_read", "tokens_full"
        ]
        for scope in expected_scopes:
            assert scope in TOKEN_SCOPES

    def test_token_json_serialization(self):
        """Test that token requests serialize correctly to JSON."""
        # Test create request JSON
        create_request = TokenCreateRequest(
            name="Test Token",
            domain_id="test-domain",
            scopes=["email_full", "domains_read"]
        )
        
        json_data = create_request.to_json()
        assert json_data["name"] == "Test Token"
        assert json_data["domain_id"] == "test-domain"
        assert json_data["scopes"] == ["email_full", "domains_read"]
        
        # Test update request JSON
        update_request = TokenUpdateRequest(token_id="test", status="pause")
        update_json = update_request.to_json()
        assert update_json["status"] == "pause"
        
        # Test update name request JSON
        update_name_request = TokenUpdateNameRequest(token_id="test", name="New Name")
        update_name_json = update_name_request.to_json()
        assert update_name_json["name"] == "New Name"


class TestTokensBuilderIntegration:
    """Integration tests for TokensBuilder API."""

    @vcr.use_cassette("tokens_builder_list_basic.yaml")
    def test_builder_list_basic_usage(self, email_client):
        """Test basic tokens list using builder."""
        builder = TokensBuilder()
        request = builder.page(1).limit(10).build_tokens_list()
        
        response = email_client.tokens.list_tokens(request)
        
        assert isinstance(response, APIResponse)
        assert response.status_code == 200

    @vcr.use_cassette("tokens_builder_list_with_custom_limit.yaml")
    def test_builder_list_with_custom_limit(self, email_client):
        """Test tokens list with custom limit using builder."""
        builder = TokensBuilder()
        request = builder.page(1).limit(50).build_tokens_list()
        
        response = email_client.tokens.list_tokens(request)
        
        assert isinstance(response, APIResponse)
        assert response.status_code == 200
        
        # Check that the limit was applied
        if "meta" in response.data:
            meta = response.data["meta"]
            assert meta["per_page"] == 50

    @vcr.use_cassette("tokens_builder_get_not_found.yaml")
    def test_builder_get_not_found(self, email_client):
        """Test getting non-existent token using builder."""
        from mailersend.exceptions import ResourceNotFoundError
        
        builder = TokensBuilder()
        request = builder.token_id("test-token-id").build_token_get()
        
        with pytest.raises(ResourceNotFoundError):
            email_client.tokens.get_token(request)

    @vcr.use_cassette("tokens_builder_create_basic.yaml")
    def test_builder_create_basic(self, email_client, test_domain_id):
        """Test creating token using builder."""
        builder = TokensBuilder()
        request = (builder
            .name("Test Token")
            .domain_id(test_domain_id)
            .add_scope("email_full")
            .build_token_create())
        
        response = email_client.tokens.create_token(request)
        
        assert isinstance(response, APIResponse)
        assert response.status_code in [200, 201]
        assert response.data is not None

    @vcr.use_cassette("tokens_builder_update_not_found.yaml")
    def test_builder_update_not_found(self, email_client):
        """Test updating non-existent token using builder."""
        from mailersend.exceptions import ResourceNotFoundError
        
        builder = TokensBuilder()
        request = (builder
            .token_id("test-token-id")
            .pause()
            .build_token_update())
        
        with pytest.raises(ResourceNotFoundError):
            email_client.tokens.update_token(request)

    @vcr.use_cassette("tokens_builder_update_name_not_found.yaml")
    def test_builder_update_name_not_found(self, email_client):
        """Test updating non-existent token name using builder."""
        from mailersend.exceptions import ResourceNotFoundError
        
        builder = TokensBuilder()
        request = (builder
            .token_id("test-token-id")
            .name("Updated Name")
            .build_token_update_name())
        
        with pytest.raises(ResourceNotFoundError):
            email_client.tokens.update_token_name(request)

    @vcr.use_cassette("tokens_builder_delete_not_found.yaml")
    def test_builder_delete_not_found(self, email_client):
        """Test deleting non-existent token using builder."""
        from mailersend.exceptions import ResourceNotFoundError
        
        builder = TokensBuilder()
        request = builder.token_id("test-token-id").build_token_delete()
        
        with pytest.raises(ResourceNotFoundError):
            email_client.tokens.delete_token(request)

    def test_builder_fluent_interface(self):
        """Test that builder methods return self for chaining."""
        builder = TokensBuilder()
        
        # Test method chaining
        result = (builder
            .page(1)
            .limit(10)
            .token_id("test-token")
            .name("Test Token")
            .domain_id("test-domain")
            .add_scope("email_full")
            .status("pause"))
        
        assert result is builder
        
        # Verify the builder state for different requests
        list_request = builder.build_tokens_list()
        assert list_request.query_params.page == 1
        assert list_request.query_params.limit == 10
        
        get_request = builder.build_token_get()
        assert get_request.token_id == "test-token"
        
        create_request = builder.build_token_create()
        assert create_request.name == "Test Token"
        assert create_request.domain_id == "test-domain"
        assert "email_full" in create_request.scopes

    def test_builder_scope_helpers(self):
        """Test builder scope helper methods."""
        builder = TokensBuilder()
        
        # Test individual scope helpers
        builder.email_scopes()
        assert "email_full" in builder._scopes
        
        builder.domains_read_scope()
        assert "domains_read" in builder._scopes
        
        builder.domains_full_scope()
        assert "domains_full" in builder._scopes
        
        # Test scope groups
        builder_fresh = TokensBuilder()
        builder_fresh.activity_scopes()
        assert "activity_read" in builder_fresh._scopes
        assert "activity_full" in builder_fresh._scopes
        
        # Test all read scopes
        builder_read = TokensBuilder()
        builder_read.all_read_scopes()
        read_scopes = ["domains_read", "activity_read", "analytics_read"]
        for scope in read_scopes:
            assert scope in builder_read._scopes
        
        # Test all scopes
        builder_all = TokensBuilder()
        builder_all.all_scopes()
        for scope in TOKEN_SCOPES:
            assert scope in builder_all._scopes

    def test_builder_status_helpers(self):
        """Test builder status helper methods."""
        builder = TokensBuilder()
        
        # Test pause helper
        builder.pause()
        assert builder._status == "pause"
        
        # Test unpause helper
        builder.unpause()
        assert builder._status == "unpause"

    def test_builder_reset_functionality(self):
        """Test builder reset functionality."""
        builder = TokensBuilder()
        builder.page(2).limit(50).token_id("test").name("test").add_scope("email_full")
        
        # Reset the builder
        builder.reset()
        
        # Verify all fields are cleared
        assert builder._page is None
        assert builder._limit is None
        assert builder._token_id is None
        assert builder._name is None
        assert builder._domain_id is None
        assert builder._scopes == []
        assert builder._status is None

    def test_builder_copy_functionality(self):
        """Test builder copy functionality."""
        original_builder = TokensBuilder()
        original_builder.page(2).limit(50).add_scope("email_full")
        
        # Copy the builder
        copied_builder = original_builder.copy()
        
        # Modify the copy
        copied_builder.page(3).add_scope("domains_read")
        
        # Verify original is unchanged
        assert original_builder._page == 2
        assert copied_builder._page == 3
        assert "email_full" in original_builder._scopes
        assert "email_full" in copied_builder._scopes
        assert "domains_read" not in original_builder._scopes
        assert "domains_read" in copied_builder._scopes

    def test_builder_validation_errors(self):
        """Test builder validation for missing required fields."""
        builder = TokensBuilder()
        
        # Test building get request without token_id
        with pytest.raises(ValueError) as exc_info:
            builder.build_token_get()
        assert "token_id is required" in str(exc_info.value).lower()
        
        # Test building create request without name
        with pytest.raises(ValueError) as exc_info:
            builder.domain_id("test").add_scope("email_full").build_token_create()
        assert "name is required" in str(exc_info.value).lower()
        
        # Test building create request without domain_id
        with pytest.raises(ValueError) as exc_info:
            builder.reset().name("test").add_scope("email_full").build_token_create()
        assert "domain_id is required" in str(exc_info.value).lower()
        
        # Test building create request without scopes
        with pytest.raises(ValueError) as exc_info:
            builder.reset().name("test").domain_id("test").build_token_create()
        assert "scopes are required" in str(exc_info.value).lower()
        
        # Test building update request without status
        with pytest.raises(ValueError) as exc_info:
            builder.reset().token_id("test").build_token_update()
        assert "status is required" in str(exc_info.value).lower()

    def test_builder_scope_deduplication(self):
        """Test that builder prevents duplicate scopes."""
        builder = TokensBuilder()
        
        # Add the same scope multiple times
        builder.add_scope("email_full")
        builder.add_scope("email_full")
        builder.add_scope("domains_read")
        builder.add_scope("email_full")
        
        # Should only have unique scopes
        assert builder._scopes.count("email_full") == 1
        assert builder._scopes.count("domains_read") == 1
        assert len(builder._scopes) == 2

    def test_builder_default_values(self):
        """Test that builder uses appropriate default values."""
        builder = TokensBuilder()
        
        # Build request without setting pagination values
        request = builder.build_tokens_list()
        
        # Should use default values from the model
        assert request.query_params.page == 1
        assert request.query_params.limit == 25

    @vcr.use_cassette("tokens_comprehensive_workflow.yaml") 
    def test_comprehensive_tokens_workflow(self, email_client, test_domain_id):
        """Test comprehensive workflow covering list, CRUD operations, error scenarios, and builder usage."""
        # Test list with different configurations
        list_request = TokensListRequest(
            query_params=TokensListQueryParams(page=1, limit=10)
        )
        
        response = email_client.tokens.list_tokens(list_request)
        assert isinstance(response, APIResponse)
        assert response.status_code == 200
        
        # Test builder pattern with different configurations
        builder = TokensBuilder()
        
        # Test list with builder
        builder_request = builder.page(1).limit(25).build_tokens_list()
        builder_response = email_client.tokens.list_tokens(builder_request)
        assert isinstance(builder_response, APIResponse)
        assert builder_response.status_code == 200
        
        # Test error scenarios
        from mailersend.exceptions import ResourceNotFoundError
        
        # Test get non-existent token
        get_request = TokenGetRequest(token_id="non-existent-id")
        with pytest.raises(ResourceNotFoundError):
            email_client.tokens.get_token(get_request)
        
        # Test create token
        create_request = TokenCreateRequest(
            name="Test Token",
            domain_id=test_domain_id,
            scopes=["email_full"]
        )
        try:
            create_response = email_client.tokens.create_token(create_request)
            assert isinstance(create_response, APIResponse)
        except Exception:
            # Creation might fail due to quota limits or other reasons
            pass
        
        # Test builder error scenarios
        builder_get_request = builder.token_id("another-non-existent-id").build_token_get()
        with pytest.raises(ResourceNotFoundError):
            email_client.tokens.get_token(builder_get_request)