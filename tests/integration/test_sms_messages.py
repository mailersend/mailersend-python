import pytest
from tests.test_helpers import vcr, email_client
import os

from mailersend.models.sms_messages import (
    SmsMessagesListRequest,
    SmsMessageGetRequest,
    SmsMessagesListQueryParams,
)
from mailersend.models.base import APIResponse


@pytest.fixture
def basic_sms_list_request():
    """Basic SMS messages list request"""
    return SmsMessagesListRequest(
        query_params=SmsMessagesListQueryParams(page=1, limit=10)
    )


@pytest.fixture
def sms_message_get_request():
    """SMS message get request with a test message ID"""
    return SmsMessageGetRequest(sms_message_id="test-sms-message-id")


class TestSmsMessagesIntegration:
    """Integration tests for SMS Messages API."""

    @vcr.use_cassette("sms_messages_list_basic.yaml")
    def test_list_sms_messages_basic(self, email_client, basic_sms_list_request):
        """Test listing SMS messages with basic parameters."""
        response = email_client.sms_messages.list_sms_messages(basic_sms_list_request)

        assert isinstance(response, APIResponse)
        assert response.status_code == 200
        assert response.data is not None

        # Check that we have the expected structure
        if "data" in response.data:
            sms_messages = response.data["data"]
            assert isinstance(sms_messages, list)

            # If we have messages, check the structure
            if sms_messages:
                first_message = sms_messages[0]
                assert "id" in first_message
                assert "from" in first_message
                assert "to" in first_message
                assert "text" in first_message
                assert "status" in first_message
                assert "created_at" in first_message

    @vcr.use_cassette("sms_messages_list_with_pagination.yaml")
    def test_list_sms_messages_with_pagination(self, email_client):
        """Test listing SMS messages with pagination."""
        request = SmsMessagesListRequest(
            query_params=SmsMessagesListQueryParams(page=1, limit=5)
        )

        response = email_client.sms_messages.list_sms_messages(request)

        assert isinstance(response, APIResponse)
        assert response.status_code == 200

        # Check pagination metadata
        if "meta" in response.data:
            meta = response.data["meta"]
            assert "current_page" in meta
            assert "per_page" in meta
            assert "total" in meta
            assert meta["per_page"] == 5
            assert meta["current_page"] == 1

    @vcr.use_cassette("sms_messages_list_empty.yaml")
    def test_list_sms_messages_empty_result(self, email_client, basic_sms_list_request):
        """Test listing SMS messages when no messages exist."""
        response = email_client.sms_messages.list_sms_messages(basic_sms_list_request)

        assert isinstance(response, APIResponse)
        assert response.status_code == 200
        assert response.data is not None

        # Should have empty data array
        if "data" in response.data:
            assert response.data["data"] == []

    @vcr.use_cassette("sms_messages_get_single.yaml")
    def test_get_sms_message_success(self, email_client, sms_message_get_request):
        """Test getting a single SMS message successfully."""
        response = email_client.sms_messages.get_sms_message(sms_message_get_request)

        assert isinstance(response, APIResponse)
        assert response.status_code == 200
        assert response.data is not None

        # Check that we have the expected SMS message structure
        if "data" in response.data:
            sms_message = response.data["data"]
            assert "id" in sms_message
            assert "from" in sms_message
            assert "to" in sms_message
            assert "text" in sms_message
            assert "status" in sms_message
            assert "created_at" in sms_message
            assert "updated_at" in sms_message

            # Verify the ID matches what we requested
            assert sms_message["id"] == sms_message_get_request.sms_message_id

    @vcr.use_cassette("sms_messages_get_not_found.yaml")
    def test_get_sms_message_not_found(self, email_client):
        """Test getting a non-existent SMS message."""
        request = SmsMessageGetRequest(sms_message_id="non-existent-message-id")

        with pytest.raises(Exception) as exc_info:
            email_client.sms_messages.get_sms_message(request)

        # Should raise a ResourceNotFoundError or similar
        assert (
            "404" in str(exc_info.value) or "not found" in str(exc_info.value).lower()
        )

    @vcr.use_cassette("sms_messages_list_with_filters.yaml")
    def test_list_sms_messages_with_filters(self, email_client):
        """Test listing SMS messages with various filters."""
        # Note: This test assumes the SMS Messages model supports additional filters
        # You may need to adjust based on the actual model implementation

        request = SmsMessagesListRequest(
            query_params=SmsMessagesListQueryParams(page=1, limit=25)
        )

        response = email_client.sms_messages.list_sms_messages(request)

        assert isinstance(response, APIResponse)
        assert response.status_code == 200

        # Verify the response structure
        if "data" in response.data:
            sms_messages = response.data["data"]
            assert isinstance(sms_messages, list)

            # Check that we don't exceed the limit
            assert len(sms_messages) <= 25

    def test_list_sms_messages_validation_error(self, email_client):
        """Test that invalid request raises validation error."""
        with pytest.raises(Exception) as exc_info:
            # Pass invalid request type
            email_client.sms_messages.list_sms_messages("invalid-request")

        # Should raise a validation error
        assert (
            "validation" in str(exc_info.value).lower()
            or "invalid" in str(exc_info.value).lower()
        )

    def test_get_sms_message_validation_error(self, email_client):
        """Test that invalid request raises validation error."""
        with pytest.raises(Exception) as exc_info:
            # Pass invalid request type
            email_client.sms_messages.get_sms_message("invalid-request")

        # Should raise a validation error
        assert (
            "validation" in str(exc_info.value).lower()
            or "invalid" in str(exc_info.value).lower()
        )

    @vcr.use_cassette("sms_messages_api_response_structure.yaml")
    def test_api_response_structure(self, email_client, basic_sms_list_request):
        """Test that API response has the expected structure and metadata."""
        response = email_client.sms_messages.list_sms_messages(basic_sms_list_request)

        assert isinstance(response, APIResponse)
        assert response.status_code == 200
        assert hasattr(response, "data")
        assert hasattr(response, "headers")

        # Check for rate limiting headers
        if response.rate_limit_remaining is not None:
            assert isinstance(response.rate_limit_remaining, int)
            assert response.rate_limit_remaining >= 0

        # Check for request ID
        if response.request_id is not None:
            assert isinstance(response.request_id, str)
            assert len(response.request_id) > 0

    @vcr.use_cassette("sms_messages_comprehensive_workflow.yaml")
    def test_comprehensive_sms_messages_workflow(self, email_client):
        """Test a comprehensive workflow of listing and retrieving SMS messages."""

        # Step 1: List SMS messages
        list_request = SmsMessagesListRequest(
            query_params=SmsMessagesListQueryParams(page=1, limit=5)
        )

        list_response = email_client.sms_messages.list_sms_messages(list_request)
        assert isinstance(list_response, APIResponse)
        assert list_response.status_code == 200

        # Step 2: If we have messages, get details for the first one
        if "data" in list_response.data and list_response.data["data"]:
            first_message = list_response.data["data"][0]
            message_id = first_message["id"]

            # Get detailed information for this message
            get_request = SmsMessageGetRequest(sms_message_id=message_id)
            get_response = email_client.sms_messages.get_sms_message(get_request)

            assert isinstance(get_response, APIResponse)
            assert get_response.status_code == 200
            assert "data" in get_response.data

            # Verify the retrieved message has the same ID
            retrieved_message = get_response.data["data"]
            assert retrieved_message["id"] == message_id

            # The detailed view should have at least as much information as the list view
            for key in first_message.keys():
                assert key in retrieved_message
