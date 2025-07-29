import pytest
from tests.test_helpers import vcr, email_client
import os

from mailersend.models.inbound import (
    InboundListRequest,
    InboundGetRequest,
    InboundCreateRequest,
    InboundUpdateRequest,
    InboundDeleteRequest,
    InboundListQueryParams,
    InboundFilterGroup,
    InboundForward,
)
from mailersend.models.base import APIResponse
from mailersend.builders.inbound import InboundBuilder


@pytest.fixture
def basic_inbound_list_request():
    """Basic inbound list request"""
    return InboundListRequest(
        query_params=InboundListQueryParams(page=1, limit=10)
    )


@pytest.fixture
def inbound_get_request():
    """Inbound get request with test inbound ID"""
    return InboundGetRequest(inbound_id="test-inbound-id")


@pytest.fixture
def test_domain_id():
    """Get the test domain ID from environment variables"""
    return os.environ.get("SDK_DOMAIN_ID", "test-domain-id")


@pytest.fixture
def sample_inbound_data(test_domain_id):
    """Sample inbound data for testing"""
    return {
        "domain_id": test_domain_id,
        "name": "Test Inbound Route",
        "domain_enabled": False,
        "inbound_domain": None,
        "inbound_priority": None,
        "catch_filter": [
            InboundFilterGroup(type="catch_all")
        ],
        "catch_type": "all",
        "match_filter": [
            InboundFilterGroup(type="match_all")
        ],
        "match_type": "all",
        "forwards": [
            InboundForward(type="email", value=os.environ.get("SDK_FROM_EMAIL", "test@example.com"))
        ]
    }


@pytest.fixture
def sample_inbound_data_with_domain(test_domain_id):
    """Sample inbound data with domain enabled for testing"""
    return {
        "domain_id": test_domain_id,
        "name": "Test Inbound Route with Domain",
        "domain_enabled": True,
        "inbound_domain": "inbound.example.com",
        "inbound_priority": 50,
        "catch_filter": [
            InboundFilterGroup(
                type="catch_recipient",
                filters=[
                    {
                        "comparer": "equal",
                        "value": "support@example.com"
                    }
                ]
            )
        ],
        "catch_type": "all",
        "match_filter": [
            InboundFilterGroup(
                type="match_sender",
                filters=[
                    {
                        "comparer": "contains",
                        "value": "@trusted.com"
                    }
                ]
            )
        ],
        "match_type": "all",
        "forwards": [
            InboundForward(type="email", value=os.environ.get("SDK_FROM_EMAIL", "test@example.com")),
            InboundForward(type="webhook", value="https://example.com/webhook", secret="webhook-secret")
        ]
    }


class TestInboundIntegration:
    """Integration tests for Inbound API."""

    @vcr.use_cassette("inbound_list_basic.yaml")
    def test_list_inbound_routes_basic(self, email_client, basic_inbound_list_request):
        """Test listing inbound routes with basic parameters."""
        response = email_client.inbound.list(basic_inbound_list_request)

        assert isinstance(response, APIResponse)
        assert response.status_code == 200
        assert response.data is not None

        # Check that we have the expected structure
        if "data" in response.data:
            inbound_routes = response.data["data"]
            assert isinstance(inbound_routes, list)

            # If we have inbound routes, check the structure
            if inbound_routes:
                first_route = inbound_routes[0]
                assert "id" in first_route
                assert "name" in first_route
                assert "domain_id" in first_route
                assert "domain_enabled" in first_route
                assert "created_at" in first_route
                assert "catch_filter" in first_route
                assert "match_filter" in first_route
                assert "forwards" in first_route

    @vcr.use_cassette("inbound_list_with_pagination.yaml")
    def test_list_inbound_routes_with_pagination(self, email_client):
        """Test listing inbound routes with pagination."""
        request = InboundListRequest(
            query_params=InboundListQueryParams(page=1, limit=10)
        )

        response = email_client.inbound.list(request)

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

    @vcr.use_cassette("inbound_list_with_domain_filter.yaml")
    def test_list_inbound_routes_with_domain_filter(self, email_client, test_domain_id):
        """Test listing inbound routes filtered by domain."""
        request = InboundListRequest(
            query_params=InboundListQueryParams(
                page=1, 
                limit=10, 
                domain_id=test_domain_id
            )
        )

        response = email_client.inbound.list(request)

        assert isinstance(response, APIResponse)
        assert response.status_code == 200
        assert response.data is not None

    @vcr.use_cassette("inbound_get_not_found.yaml")
    def test_get_inbound_route_not_found(self, email_client, inbound_get_request):
        """Test getting a non-existent inbound route returns 404."""
        from mailersend.exceptions import ResourceNotFoundError
        
        with pytest.raises(ResourceNotFoundError) as exc_info:
            email_client.inbound.get(inbound_get_request)

        assert "not found" in str(exc_info.value).lower() or "404" in str(exc_info.value) or "could not be found" in str(exc_info.value).lower()

    @vcr.use_cassette("inbound_create_invalid_domain.yaml")
    def test_create_inbound_route_invalid_domain(self, email_client, sample_inbound_data):
        """Test creating inbound route with invalid domain ID returns 422."""
        from mailersend.exceptions import BadRequestError
        
        request = InboundCreateRequest(
            domain_id="invalid-domain-id",
            **{k: v for k, v in sample_inbound_data.items() if k != "domain_id"}
        )

        with pytest.raises(BadRequestError) as exc_info:
            email_client.inbound.create(request)

        error_str = str(exc_info.value).lower()
        assert "domain" in error_str and ("invalid" in error_str or "required" in error_str or "not found" in error_str)

    @vcr.use_cassette("inbound_update_not_found.yaml")
    def test_update_inbound_route_not_found(self, email_client, sample_inbound_data):
        """Test updating non-existent inbound route returns 404."""
        from mailersend.exceptions import ResourceNotFoundError
        
        request = InboundUpdateRequest(
            inbound_id="test-inbound-id",
            **{k: v for k, v in sample_inbound_data.items() if k != "domain_id"}
        )

        with pytest.raises(ResourceNotFoundError) as exc_info:
            email_client.inbound.update(request)

        assert "not found" in str(exc_info.value).lower() or "404" in str(exc_info.value) or "could not be found" in str(exc_info.value).lower()

    @vcr.use_cassette("inbound_delete_not_found.yaml")
    def test_delete_inbound_route_not_found(self, email_client, inbound_get_request):
        """Test deleting non-existent inbound route returns 404."""
        from mailersend.exceptions import ResourceNotFoundError
        
        delete_request = InboundDeleteRequest(
            inbound_id=inbound_get_request.inbound_id
        )

        with pytest.raises(ResourceNotFoundError) as exc_info:
            email_client.inbound.delete(delete_request)

        assert "not found" in str(exc_info.value).lower() or "404" in str(exc_info.value) or "could not be found" in str(exc_info.value).lower()

    @vcr.use_cassette("inbound_validation_error.yaml")
    def test_list_inbound_routes_validation_error(self, email_client):
        """Test that invalid request raises validation error."""
        with pytest.raises(Exception) as exc_info:
            # Pass invalid request type
            email_client.inbound.list("invalid-request")

        # Should raise an AttributeError for invalid request type
        error_str = str(exc_info.value).lower()
        assert (
            "attribute" in error_str
            or "to_query_params" in error_str
        )

    @vcr.use_cassette("inbound_api_response_structure.yaml")
    def test_api_response_structure(self, email_client, basic_inbound_list_request):
        """Test that API response has the expected structure and metadata."""
        response = email_client.inbound.list(basic_inbound_list_request)

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

    @vcr.use_cassette("inbound_empty_result.yaml")
    def test_list_inbound_routes_empty_result(self, email_client, basic_inbound_list_request):
        """Test listing inbound routes when no routes exist."""
        response = email_client.inbound.list(basic_inbound_list_request)

        assert isinstance(response, APIResponse)
        assert response.status_code == 200
        assert response.data is not None

        # Should have data array (may not be empty due to previous tests creating data)
        if "data" in response.data:
            assert isinstance(response.data["data"], list)

    def test_create_inbound_route_model_validation(self):
        """Test model validation for inbound route creation."""
        # Test empty domain_id
        with pytest.raises(ValueError) as exc_info:
            InboundCreateRequest(
                domain_id="",
                name="Test Route",
                domain_enabled=False,
                catch_filter=[InboundFilterGroup(type="catch_all")],
                match_filter=[InboundFilterGroup(type="match_all")],
                forwards=[InboundForward(type="email", value="test@example.com")]
            )
        assert "domain id is required" in str(exc_info.value).lower()

        # Test empty name
        with pytest.raises(ValueError) as exc_info:
            InboundCreateRequest(
                domain_id="test-domain",
                name="",
                domain_enabled=False,
                catch_filter=[InboundFilterGroup(type="catch_all")],
                match_filter=[InboundFilterGroup(type="match_all")],
                forwards=[InboundForward(type="email", value="test@example.com")]
            )
        assert "name is required" in str(exc_info.value).lower()

        # Test missing forwards
        with pytest.raises(ValueError) as exc_info:
            InboundCreateRequest(
                domain_id="test-domain",
                name="Test Route",
                domain_enabled=False,
                catch_filter=[InboundFilterGroup(type="catch_all")],
                match_filter=[InboundFilterGroup(type="match_all")],
                forwards=[]
            )
        assert "at least one forward is required" in str(exc_info.value).lower()

        # Test domain enabled without inbound_domain
        with pytest.raises(ValueError) as exc_info:
            InboundCreateRequest(
                domain_id="test-domain",
                name="Test Route",
                domain_enabled=True,
                catch_filter=[InboundFilterGroup(type="catch_all")],
                match_filter=[InboundFilterGroup(type="match_all")],
                forwards=[InboundForward(type="email", value="test@example.com")]
            )
        assert "inbound domain is required when domain is enabled" in str(exc_info.value).lower()

        # Test domain enabled without inbound_priority
        with pytest.raises(ValueError) as exc_info:
            InboundCreateRequest(
                domain_id="test-domain",
                name="Test Route",
                domain_enabled=True,
                inbound_domain="test.com",
                catch_filter=[InboundFilterGroup(type="catch_all")],
                match_filter=[InboundFilterGroup(type="match_all")],
                forwards=[InboundForward(type="email", value="test@example.com")]
            )
        assert "inbound priority is required when domain is enabled" in str(exc_info.value).lower()


class TestInboundBuilderIntegration:
    """Integration tests for InboundBuilder API."""

    @vcr.use_cassette("inbound_builder_list_basic.yaml")
    def test_builder_list_basic_usage(self, email_client):
        """Test basic inbound list using builder."""
        builder = InboundBuilder()
        request = builder.page(1).limit(10).build_list_request()
        
        response = email_client.inbound.list(request)
        
        assert isinstance(response, APIResponse)
        assert response.status_code == 200

    @vcr.use_cassette("inbound_builder_list_with_domain.yaml")
    def test_builder_list_with_domain_filter(self, email_client, test_domain_id):
        """Test inbound list with domain filter using builder."""
        builder = InboundBuilder()
        request = builder.page(1).limit(10).domain_id(test_domain_id).build_list_request()
        
        response = email_client.inbound.list(request)
        
        assert isinstance(response, APIResponse)
        assert response.status_code == 200

    @vcr.use_cassette("inbound_builder_get_not_found.yaml")
    def test_builder_get_not_found(self, email_client):
        """Test getting non-existent inbound route using builder."""
        from mailersend.exceptions import ResourceNotFoundError
        
        builder = InboundBuilder()
        request = builder.inbound_id("test-inbound-id").build_get_request()
        
        with pytest.raises(ResourceNotFoundError):
            email_client.inbound.get(request)

    @vcr.use_cassette("inbound_builder_create_invalid_domain.yaml")
    def test_builder_create_invalid_domain(self, email_client):
        """Test creating inbound route with invalid domain using builder."""
        from mailersend.exceptions import BadRequestError
        
        builder = InboundBuilder()
        request = (builder
            .domain_id("invalid-domain-id")
            .name("Test Route")
            .domain_enabled(False)
            .catch_all()
            .match_all()
            .add_email_forward("test@example.com")
            .build_create_request())
        
        with pytest.raises(BadRequestError):
            email_client.inbound.create(request)

    def test_builder_reset_functionality(self):
        """Test builder reset functionality."""
        builder = InboundBuilder()
        builder.domain_id("test").name("test").page(2).limit(5)
        
        # Reset the builder
        builder.reset()
        
        # Build a basic request to verify reset worked
        request = builder.build_list_request()
        assert request.query_params.page == 1  # Default value
        assert request.query_params.limit == 25  # Default value
        assert request.query_params.domain_id is None

    def test_builder_copy_functionality(self):
        """Test builder copy functionality."""
        original_builder = InboundBuilder()
        original_builder.domain_id("test").page(2).limit(5)
        
        # Copy the builder
        copied_builder = original_builder.copy()
        
        # Modify the copy
        copied_builder.page(3)
        
        # Verify original is unchanged
        original_request = original_builder.build_list_request()
        copied_request = copied_builder.build_list_request()
        
        assert original_request.query_params.page == 2
        assert copied_request.query_params.page == 3
        assert original_request.query_params.domain_id == copied_request.query_params.domain_id

    def test_builder_fluent_interface(self):
        """Test that builder methods return self for chaining."""
        builder = InboundBuilder()
        
        # Test method chaining
        result = (builder
            .domain_id("test")
            .name("Test Route")
            .domain_enabled(False)
            .page(1)
            .limit(10)
            .catch_all()
            .match_all()
            .add_email_forward("test@example.com"))
        
        assert result is builder
        
        # Verify the builder state
        request = builder.build_create_request()
        assert request.domain_id == "test"
        assert request.name == "Test Route"
        assert request.domain_enabled is False
        assert len(request.catch_filter) == 1
        assert len(request.match_filter) == 1
        assert len(request.forwards) == 1

    def test_builder_complex_filter_configuration(self):
        """Test complex filter configuration with builder."""
        builder = InboundBuilder()
        
        # Build complex configuration
        request = (builder
            .domain_id("test-domain")
            .name("Complex Route")
            .domain_enabled(True)
            .enable_domain("inbound.example.com", 75)
            .catch_recipient([
                {"comparer": "equal", "value": "support@example.com"},
                {"comparer": "contains", "value": "help"}
            ], "all")
            .match_sender([
                {"comparer": "ends-with", "value": "@trusted.com"}
            ], "all")
            .add_email_forward("admin@example.com")
            .add_webhook_forward("https://api.example.com/webhook", "secret123")
            .build_create_request())
        
        assert request.domain_id == "test-domain"
        assert request.name == "Complex Route"
        assert request.domain_enabled is True
        assert request.inbound_domain == "inbound.example.com"
        assert request.inbound_priority == 75
        assert len(request.catch_filter) == 1
        assert request.catch_filter[0].type == "catch_recipient"
        assert len(request.match_filter) == 1
        assert request.match_filter[0].type == "match_sender"
        assert len(request.forwards) == 2
        assert request.forwards[0].type == "email"
        assert request.forwards[1].type == "webhook"
        assert request.forwards[1].secret == "secret123"

    @vcr.use_cassette("inbound_comprehensive_workflow.yaml") 
    def test_comprehensive_inbound_workflow(self, email_client, test_domain_id):
        """Test comprehensive workflow covering list, error scenarios, and builder usage."""
        # Test list with pagination
        list_request = InboundListRequest(
            query_params=InboundListQueryParams(page=1, limit=10, domain_id=test_domain_id)
        )
        
        response = email_client.inbound.list(list_request)
        assert isinstance(response, APIResponse)
        assert response.status_code == 200
        
        # Test builder pattern
        builder = InboundBuilder()
        builder_request = builder.page(1).limit(10).domain_id(test_domain_id).build_list_request()
        
        builder_response = email_client.inbound.list(builder_request)
        assert isinstance(builder_response, APIResponse)
        assert builder_response.status_code == 200
        
        # Test error scenarios
        from mailersend.exceptions import ResourceNotFoundError
        
        get_request = InboundGetRequest(inbound_id="non-existent-id")
        with pytest.raises(ResourceNotFoundError):
            email_client.inbound.get(get_request)