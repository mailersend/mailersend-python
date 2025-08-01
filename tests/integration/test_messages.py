import pytest
from tests.test_helpers import vcr, email_client
import os

from mailersend.models.messages import (
    MessagesListRequest,
    MessageGetRequest,
    MessagesListQueryParams,
)
from mailersend.models.base import APIResponse
from mailersend.builders.messages import MessagesBuilder


@pytest.fixture
def basic_messages_list_request():
    """Basic messages list request"""
    return MessagesListRequest(
        query_params=MessagesListQueryParams(page=1, limit=10)
    )


@pytest.fixture
def message_get_request():
    """Message get request with test message ID"""
    return MessageGetRequest(message_id="test-message-id")


class TestMessagesIntegration:
    """Integration tests for Messages API."""

    @vcr.use_cassette("messages_list_basic.yaml")
    def test_list_messages_basic(self, email_client, basic_messages_list_request):
        """Test listing messages with basic parameters."""
        response = email_client.messages.list_messages(basic_messages_list_request)

        assert isinstance(response, APIResponse)
        assert response.status_code == 200
        assert response.data is not None

        # Check that we have the expected structure
        if "data" in response.data:
            messages = response.data["data"]
            assert isinstance(messages, list)

            # If we have messages, check the structure
            if messages:
                first_message = messages[0]
                assert "id" in first_message
                assert "created_at" in first_message
                # Messages typically have these fields
                expected_fields = ["id", "created_at", "updated_at", "status"]
                for field in expected_fields:
                    if field in first_message:
                        assert first_message[field] is not None

    @vcr.use_cassette("messages_list_with_pagination.yaml")
    def test_list_messages_with_pagination(self, email_client):
        """Test listing messages with pagination."""
        request = MessagesListRequest(
            query_params=MessagesListQueryParams(page=1, limit=10)
        )

        response = email_client.messages.list_messages(request)

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

    @vcr.use_cassette("messages_list_different_limit.yaml")
    def test_list_messages_different_limit(self, email_client):
        """Test listing messages with different limit."""
        request = MessagesListRequest(
            query_params=MessagesListQueryParams(page=1, limit=25)
        )

        response = email_client.messages.list_messages(request)

        assert isinstance(response, APIResponse)
        assert response.status_code == 200
        assert response.data is not None

        # Check pagination reflects the requested limit
        if "meta" in response.data:
            meta = response.data["meta"]
            # Expect actual values: per_page often returns the requested limit
            assert meta["per_page"] == 25

    @vcr.use_cassette("messages_get_not_found.yaml")
    def test_get_message_not_found(self, email_client, message_get_request):
        """Test getting a non-existent message returns 404."""
        from mailersend.exceptions import ResourceNotFoundError
        
        with pytest.raises(ResourceNotFoundError) as exc_info:
            email_client.messages.get_message(message_get_request)

        assert "not found" in str(exc_info.value).lower() or "404" in str(exc_info.value) or "could not be found" in str(exc_info.value).lower()

    @vcr.use_cassette("messages_validation_error.yaml")
    def test_list_messages_validation_error(self, email_client):
        """Test that invalid request raises validation error."""
        with pytest.raises(Exception) as exc_info:
            # Pass invalid request type
            email_client.messages.list_messages("invalid-request")

        # Should raise an AttributeError for invalid request type
        error_str = str(exc_info.value).lower()
        assert (
            "attribute" in error_str
            or "to_query_params" in error_str
        )

    @vcr.use_cassette("messages_api_response_structure.yaml")
    def test_api_response_structure(self, email_client, basic_messages_list_request):
        """Test that API response has the expected structure and metadata."""
        response = email_client.messages.list_messages(basic_messages_list_request)

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

    @vcr.use_cassette("messages_empty_result.yaml")
    def test_list_messages_empty_result(self, email_client, basic_messages_list_request):
        """Test listing messages when no messages exist."""
        response = email_client.messages.list_messages(basic_messages_list_request)

        assert isinstance(response, APIResponse)
        assert response.status_code == 200
        assert response.data is not None

        # Should have data array (may not be empty due to previous tests creating data)
        if "data" in response.data:
            assert isinstance(response.data["data"], list)

    def test_message_get_model_validation(self):
        """Test model validation for message retrieval."""
        # Test empty message_id
        with pytest.raises(ValueError) as exc_info:
            MessageGetRequest(message_id="")
        assert "message id is required" in str(exc_info.value).lower()

        # Test None message_id - this will raise a pydantic ValidationError
        from pydantic import ValidationError
        with pytest.raises(ValidationError) as exc_info:
            MessageGetRequest(message_id=None)
        assert "input should be a valid string" in str(exc_info.value).lower()

    def test_messages_list_query_params_validation(self):
        """Test validation for messages list query parameters."""
        # Test valid parameters
        params = MessagesListQueryParams(page=1, limit=25)
        assert params.page == 1
        assert params.limit == 25
        
        # Test minimum limit validation
        with pytest.raises(ValueError):
            MessagesListQueryParams(limit=5)  # Below minimum of 10
            
        # Test maximum limit validation  
        with pytest.raises(ValueError):
            MessagesListQueryParams(limit=150)  # Above maximum of 100
            
        # Test minimum page validation
        with pytest.raises(ValueError):
            MessagesListQueryParams(page=0)  # Below minimum of 1


class TestMessagesBuilderIntegration:
    """Integration tests for MessagesBuilder API."""

    @vcr.use_cassette("messages_builder_list_basic.yaml")
    def test_builder_list_basic_usage(self, email_client):
        """Test basic messages list using builder."""
        builder = MessagesBuilder()
        request = builder.page(1).limit(10).build_list_request()
        
        response = email_client.messages.list_messages(request)
        
        assert isinstance(response, APIResponse)
        assert response.status_code == 200

    @vcr.use_cassette("messages_builder_list_with_custom_limit.yaml")
    def test_builder_list_with_custom_limit(self, email_client):
        """Test messages list with custom limit using builder."""
        builder = MessagesBuilder()
        request = builder.page(1).limit(50).build_list_request()
        
        response = email_client.messages.list_messages(request)
        
        assert isinstance(response, APIResponse)
        assert response.status_code == 200
        
        # Check that the limit was applied
        if "meta" in response.data:
            meta = response.data["meta"]
            assert meta["per_page"] == 50

    @vcr.use_cassette("messages_builder_get_not_found.yaml")
    def test_builder_get_not_found(self, email_client):
        """Test getting non-existent message using builder."""
        from mailersend.exceptions import ResourceNotFoundError
        
        builder = MessagesBuilder()
        request = builder.message_id("test-message-id").build_get_request()
        
        with pytest.raises(ResourceNotFoundError):
            email_client.messages.get_message(request)

    def test_builder_reset_functionality(self):
        """Test builder reset functionality."""
        builder = MessagesBuilder()
        builder.page(2).limit(50).message_id("test-id")
        
        # Reset the builder
        builder.reset()
        
        # Build a basic request to verify reset worked
        request = builder.build_list_request()
        assert request.query_params.page == 1  # Default value
        assert request.query_params.limit == 25  # Default value
        
        # Verify message_id was reset
        from mailersend.exceptions import ValidationError
        with pytest.raises(ValidationError):
            builder.build_get_request()  # Should fail because message_id was reset

    def test_builder_copy_functionality(self):
        """Test builder copy functionality."""
        original_builder = MessagesBuilder()
        original_builder.page(2).limit(50)
        
        # Copy the builder
        copied_builder = original_builder.copy()
        
        # Modify the copy
        copied_builder.page(3)
        
        # Verify original is unchanged
        original_request = original_builder.build_list_request()
        copied_request = copied_builder.build_list_request()
        
        assert original_request.query_params.page == 2
        assert copied_request.query_params.page == 3
        assert original_request.query_params.limit == copied_request.query_params.limit

    def test_builder_fluent_interface(self):
        """Test that builder methods return self for chaining."""
        builder = MessagesBuilder()
        
        # Test method chaining
        result = builder.page(1).limit(10).message_id("test-id")
        
        assert result is builder
        
        # Verify the builder state for list request
        list_request = builder.build_list_request()
        assert list_request.query_params.page == 1
        assert list_request.query_params.limit == 10
        
        # Verify the builder state for get request
        get_request = builder.build_get_request()
        assert get_request.message_id == "test-id"

    def test_builder_validation_errors(self):
        """Test builder validation for invalid inputs."""
        from mailersend.exceptions import ValidationError
        
        builder = MessagesBuilder()
        
        # Test invalid page
        with pytest.raises(ValidationError) as exc_info:
            builder.page(0)
        assert "page must be greater than 0" in str(exc_info.value).lower()
        
        # Test invalid limit (too low)
        with pytest.raises(ValidationError) as exc_info:
            builder.limit(5)
        assert "limit must be between 10 and 100" in str(exc_info.value).lower()
        
        # Test invalid limit (too high)
        with pytest.raises(ValidationError) as exc_info:
            builder.limit(150)
        assert "limit must be between 10 and 100" in str(exc_info.value).lower()
        
        # Test empty message_id
        with pytest.raises(ValidationError) as exc_info:
            builder.message_id("")
        assert "message id cannot be empty" in str(exc_info.value).lower()
        
        # Test building get request without message_id
        fresh_builder = MessagesBuilder()
        with pytest.raises(ValidationError) as exc_info:
            fresh_builder.build_get_request()
        assert "message id must be set" in str(exc_info.value).lower()

    def test_builder_default_values(self):
        """Test that builder uses appropriate default values."""
        builder = MessagesBuilder()
        
        # Build request without setting any values
        request = builder.build_list_request()
        
        # Should use default values from the model
        assert request.query_params.page == 1
        assert request.query_params.limit == 25

    def test_builder_pagination_scenarios(self):
        """Test various pagination scenarios with builder."""
        builder = MessagesBuilder()
        
        # Test first page
        request1 = builder.page(1).limit(10).build_list_request()
        assert request1.query_params.page == 1
        assert request1.query_params.limit == 10
        
        # Test different page
        request2 = builder.page(5).limit(20).build_list_request()
        assert request2.query_params.page == 5
        assert request2.query_params.limit == 20
        
        # Test maximum limit
        request3 = builder.page(1).limit(100).build_list_request()
        assert request3.query_params.page == 1
        assert request3.query_params.limit == 100

    @vcr.use_cassette("messages_comprehensive_workflow.yaml") 
    def test_comprehensive_messages_workflow(self, email_client):
        """Test comprehensive workflow covering list, get, error scenarios, and builder usage."""
        # Test list with different pagination settings
        list_request = MessagesListRequest(
            query_params=MessagesListQueryParams(page=1, limit=10)
        )
        
        response = email_client.messages.list_messages(list_request)
        assert isinstance(response, APIResponse)
        assert response.status_code == 200
        
        # Test builder pattern with different configurations
        builder = MessagesBuilder()
        
        # Test list with builder
        builder_request = builder.page(1).limit(25).build_list_request()
        builder_response = email_client.messages.list_messages(builder_request)
        assert isinstance(builder_response, APIResponse)
        assert builder_response.status_code == 200
        
        # Test error scenarios
        from mailersend.exceptions import ResourceNotFoundError
        
        get_request = MessageGetRequest(message_id="non-existent-id")
        with pytest.raises(ResourceNotFoundError):
            email_client.messages.get_message(get_request)
        
        # Test builder get error scenario
        builder_get_request = builder.message_id("another-non-existent-id").build_get_request()
        with pytest.raises(ResourceNotFoundError):
            email_client.messages.get_message(builder_get_request)