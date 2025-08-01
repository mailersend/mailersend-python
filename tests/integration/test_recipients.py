import pytest
from tests.test_helpers import vcr, email_client
import os

from mailersend.models.recipients import (
    RecipientsListRequest,
    RecipientGetRequest,
    RecipientDeleteRequest,
    SuppressionListRequest,
    SuppressionAddRequest,
    SuppressionDeleteRequest,
    RecipientsListQueryParams,
    SuppressionListQueryParams,
)
from mailersend.models.base import APIResponse


@pytest.fixture
def basic_recipients_list_request():
    """Basic recipients list request"""
    return RecipientsListRequest(
        query_params=RecipientsListQueryParams(page=1, limit=10)
    )


@pytest.fixture
def recipient_get_request():
    """Recipient get request with test recipient ID"""
    return RecipientGetRequest(recipient_id="test-recipient-id")


@pytest.fixture
def suppression_list_request():
    """Suppression list request with test domain ID"""
    return SuppressionListRequest(
        domain_id="test-domain-id",
        query_params=SuppressionListQueryParams(page=1, limit=10),
    )


@pytest.fixture
def sample_recipients_list():
    """Sample recipients list for testing"""
    return ["test1@example.com", "test2@example.com", "test3@example.com"]


class TestRecipientsIntegration:
    """Integration tests for Recipients API."""

    @vcr.use_cassette("recipients_list_basic.yaml")
    def test_list_recipients_basic(self, email_client, basic_recipients_list_request):
        """Test listing recipients with basic parameters."""
        response = email_client.recipients.list_recipients(
            basic_recipients_list_request
        )

        assert isinstance(response, APIResponse)
        assert response.status_code == 200
        assert response.data is not None

        # Check that we have the expected structure
        if "data" in response.data:
            recipients = response.data["data"]
            assert isinstance(recipients, list)

            # If we have recipients, check the structure
            if recipients:
                first_recipient = recipients[0]
                assert "id" in first_recipient
                assert "email" in first_recipient
                assert "created_at" in first_recipient
                assert "updated_at" in first_recipient

    @vcr.use_cassette("recipients_list_with_pagination.yaml")
    def test_list_recipients_with_pagination(self, email_client):
        """Test listing recipients with pagination."""
        request = RecipientsListRequest(
            query_params=RecipientsListQueryParams(page=1, limit=10)
        )

        response = email_client.recipients.list_recipients(request)

        assert isinstance(response, APIResponse)
        assert response.status_code == 200

        # Check pagination metadata
        if "meta" in response.data:
            meta = response.data["meta"]
            assert "current_page" in meta
            assert "per_page" in meta
            # API may or may not include total count in meta
            assert meta["per_page"] == 10
            assert meta["current_page"] == 1

    @vcr.use_cassette("recipients_get_single.yaml")
    def test_get_recipient_not_found_with_test_id(self, email_client, recipient_get_request):
        """Test getting a non-existent recipient returns 404."""
        from mailersend.exceptions import ResourceNotFoundError
        
        with pytest.raises(ResourceNotFoundError) as exc_info:
            email_client.recipients.get_recipient(recipient_get_request)

        assert "not found" in str(exc_info.value).lower() or "404" in str(exc_info.value)

    @vcr.use_cassette("recipients_delete_success.yaml")
    def test_delete_recipient_not_found_with_test_id(self, email_client, recipient_get_request):
        """Test deleting a non-existent recipient returns 404."""
        from mailersend.exceptions import ResourceNotFoundError
        
        delete_request = RecipientDeleteRequest(
            recipient_id=recipient_get_request.recipient_id
        )

        with pytest.raises(ResourceNotFoundError) as exc_info:
            email_client.recipients.delete_recipient(delete_request)

        assert "not found" in str(exc_info.value).lower() or "404" in str(exc_info.value)

    # Suppression Lists Tests

    @vcr.use_cassette("recipients_blocklist_basic.yaml")
    def test_get_blocklist_basic(self, email_client, suppression_list_request):
        """Test getting blocklist with basic parameters."""
        response = email_client.recipients.list_blocklist(suppression_list_request)

        assert isinstance(response, APIResponse)
        assert response.status_code == 200
        assert response.data is not None

        # Check that we have the expected structure
        if "data" in response.data:
            blocklist = response.data["data"]
            assert isinstance(blocklist, list)

            # If we have blocked recipients, check the structure
            if blocklist:
                first_blocked = blocklist[0]
                assert "id" in first_blocked
                assert "email" in first_blocked
                assert "created_at" in first_blocked

    @vcr.use_cassette("recipients_hard_bounces_basic.yaml")
    def test_get_hard_bounces_basic(self, email_client, suppression_list_request):
        """Test getting hard bounces with basic parameters."""
        response = email_client.recipients.list_hard_bounces(suppression_list_request)

        assert isinstance(response, APIResponse)
        assert response.status_code == 200
        assert response.data is not None

        # Check that we have the expected structure
        if "data" in response.data:
            hard_bounces = response.data["data"]
            assert isinstance(hard_bounces, list)

            # If we have hard bounces, check the structure
            if hard_bounces:
                first_bounce = hard_bounces[0]
                assert "id" in first_bounce
                # Email is nested in recipient object
                assert "recipient" in first_bounce
                assert "email" in first_bounce["recipient"]
                assert "created_at" in first_bounce

    @vcr.use_cassette("recipients_spam_complaints_basic.yaml")
    def test_get_spam_complaints_basic(self, email_client, suppression_list_request):
        """Test getting spam complaints with basic parameters."""
        response = email_client.recipients.list_spam_complaints(suppression_list_request)

        assert isinstance(response, APIResponse)
        assert response.status_code == 200
        assert response.data is not None

        # Check that we have the expected structure
        if "data" in response.data:
            spam_complaints = response.data["data"]
            assert isinstance(spam_complaints, list)

            # If we have spam complaints, check the structure
            if spam_complaints:
                first_complaint = spam_complaints[0]
                assert "id" in first_complaint
                assert "email" in first_complaint
                assert "created_at" in first_complaint

    @vcr.use_cassette("recipients_unsubscribes_basic.yaml")
    def test_get_unsubscribes_basic(self, email_client, suppression_list_request):
        """Test getting unsubscribes with basic parameters."""
        response = email_client.recipients.list_unsubscribes(suppression_list_request)

        assert isinstance(response, APIResponse)
        assert response.status_code == 200
        assert response.data is not None

        # Check that we have the expected structure
        if "data" in response.data:
            unsubscribes = response.data["data"]
            assert isinstance(unsubscribes, list)

            # If we have unsubscribes, check the structure
            if unsubscribes:
                first_unsubscribe = unsubscribes[0]
                assert "id" in first_unsubscribe
                assert "email" in first_unsubscribe
                assert "created_at" in first_unsubscribe

    @vcr.use_cassette("recipients_add_to_blocklist.yaml")
    def test_add_to_blocklist_invalid_domain(self, email_client):
        """Test adding to blocklist with invalid domain ID returns 422."""
        from mailersend.exceptions import BadRequestError
        from mailersend.models.recipients import SuppressionAddRequest
        
        request = SuppressionAddRequest(
            domain_id="test-domain-id",  # Invalid domain ID
            recipients=["test@example.com"],
        )

        with pytest.raises(BadRequestError) as exc_info:
            email_client.recipients.add_to_blocklist(request)

        error_str = str(exc_info.value).lower()
        assert "domain" in error_str and ("invalid" in error_str or "required" in error_str)

    @vcr.use_cassette("recipients_add_hard_bounces.yaml")
    def test_add_hard_bounces_invalid_domain(self, email_client):
        """Test adding hard bounces with invalid domain ID returns 422."""
        from mailersend.exceptions import BadRequestError
        from mailersend.models.recipients import SuppressionAddRequest
        
        request = SuppressionAddRequest(
            domain_id="test-domain-id",  # Invalid domain ID
            recipients=["test@example.com"],
        )

        with pytest.raises(BadRequestError) as exc_info:
            email_client.recipients.add_hard_bounces(request)

        error_str = str(exc_info.value).lower()
        assert "domain" in error_str and ("invalid" in error_str or "required" in error_str)

    @vcr.use_cassette("recipients_add_spam_complaints.yaml")
    def test_add_spam_complaints_invalid_domain(self, email_client):
        """Test adding spam complaints with invalid domain ID returns 422."""
        from mailersend.exceptions import BadRequestError
        from mailersend.models.recipients import SuppressionAddRequest
        
        request = SuppressionAddRequest(
            domain_id="test-domain-id",  # Invalid domain ID
            recipients=["test@example.com"],
        )

        with pytest.raises(BadRequestError) as exc_info:
            email_client.recipients.add_spam_complaints(request)

        error_str = str(exc_info.value).lower()
        assert "domain" in error_str and ("invalid" in error_str or "required" in error_str)

    @vcr.use_cassette("recipients_add_unsubscribes.yaml")
    def test_add_unsubscribes_invalid_domain(self, email_client):
        """Test adding unsubscribes with invalid domain ID returns 422."""
        from mailersend.exceptions import BadRequestError
        from mailersend.models.recipients import SuppressionAddRequest
        
        request = SuppressionAddRequest(
            domain_id="test-domain-id",  # Invalid domain ID
            recipients=["test@example.com"],
        )

        with pytest.raises(BadRequestError) as exc_info:
            email_client.recipients.add_unsubscribes(request)

        error_str = str(exc_info.value).lower()
        assert "domain" in error_str and ("invalid" in error_str or "required" in error_str)

    @vcr.use_cassette("recipients_delete_from_blocklist.yaml")
    def test_delete_from_blocklist_invalid_domain(self, email_client):
        """Test deleting from blocklist with invalid domain ID returns 422."""
        from mailersend.exceptions import BadRequestError
        from mailersend.models.recipients import SuppressionDeleteRequest
        
        request = SuppressionDeleteRequest(
            domain_id="test-domain-id",  # Invalid domain ID
            ids=["test-id"],
        )

        with pytest.raises(BadRequestError) as exc_info:
            email_client.recipients.delete_from_blocklist(request)

        error_str = str(exc_info.value).lower()
        assert "domain" in error_str and ("invalid" in error_str or "required" in error_str)

    @vcr.use_cassette("recipients_comprehensive_workflow.yaml")
    def test_comprehensive_recipients_workflow_invalid_domain(self, email_client):
        """Test comprehensive workflow with invalid domain ID returns errors."""
        from mailersend.exceptions import BadRequestError
        from mailersend.models.recipients import SuppressionAddRequest
        
        # Step 1: Try to add recipient to blocklist (should fail with invalid domain)
        add_request = SuppressionAddRequest(
            domain_id="test-domain-id",  # Invalid domain ID
            recipients=["workflow-test@example.com"],
        )

        with pytest.raises(BadRequestError) as exc_info:
            email_client.recipients.add_to_blocklist(add_request)

        error_str = str(exc_info.value).lower()
        assert "domain" in error_str and ("invalid" in error_str or "required" in error_str)

    @vcr.use_cassette("recipients_api_response_structure.yaml")
    def test_api_response_structure(self, email_client, basic_recipients_list_request):
        """Test that API response has the expected structure and metadata."""
        response = email_client.recipients.list_recipients(
            basic_recipients_list_request
        )

        assert isinstance(response, APIResponse)
        assert response.status_code == 200
        assert hasattr(response, "data")
        assert hasattr(response, "headers")

        # Check for rate limiting headers
        if response.rate_limit_remaining is not None:
            assert isinstance(response.rate_limit_remaining, int)
            # Rate limit remaining can be -1 for unlimited plans

        # Check for request ID
        if response.request_id is not None:
            assert isinstance(response.request_id, str)
            assert len(response.request_id) > 0

    def test_list_recipients_validation_error(self, email_client):
        """Test that invalid request raises validation error."""
        with pytest.raises(Exception) as exc_info:
            # Pass invalid request type
            email_client.recipients.list_recipients("invalid-request")

        # Should raise an AttributeError for invalid request type
        error_str = str(exc_info.value).lower()
        assert (
            "attribute" in error_str
            or "to_query_params" in error_str
        )

    @vcr.use_cassette("recipients_empty_list.yaml")
    def test_list_recipients_empty_result(
        self, email_client, basic_recipients_list_request
    ):
        """Test listing recipients when no recipients exist."""
        response = email_client.recipients.list_recipients(
            basic_recipients_list_request
        )

        assert isinstance(response, APIResponse)
        assert response.status_code == 200
        assert response.data is not None

        # Should have data array (may not be empty due to previous tests creating data)
        if "data" in response.data:
            assert isinstance(response.data["data"], list)
