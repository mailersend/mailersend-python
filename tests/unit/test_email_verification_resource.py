"""Tests for Email Verification API resource."""

from unittest.mock import Mock, patch
import pytest

from mailersend.resources.email_verification import EmailVerification
from mailersend.models.base import APIResponse
from mailersend.models.email_verification import (
    EmailVerifyRequest,
    EmailVerifyAsyncRequest,
    EmailVerificationAsyncStatusRequest,
    EmailVerificationListsRequest,
    EmailVerificationGetRequest,
    EmailVerificationCreateRequest,
    EmailVerificationVerifyRequest,
    EmailVerificationResultsRequest,
)


class TestEmailVerification:
    """Test EmailVerification resource class."""

    def setup_method(self):
        """Set up test fixtures."""
        self.mock_client = Mock()
        self.resource = EmailVerification(self.mock_client)
        self.mock_response = Mock(spec=APIResponse)
        self.mock_client.request.return_value = self.mock_response

    def test_initialization(self):
        """Test resource initialization."""
        assert self.resource.client is self.mock_client

    def test_verify_email(self):
        """Test verify_email method."""
        request = EmailVerifyRequest(email="test@example.com")

        with patch('mailersend.resources.email_verification.logger') as mock_logger:
            result = self.resource.verify_email(request)

        assert result is self.mock_response
        self.mock_client.request.assert_called_once_with(
            "POST",
            "email-verification/verify",
            json={"email": "test@example.com"}
        )
        mock_logger.info.assert_called_once_with("Verifying email address: test@example.com")

    def test_verify_email_async(self):
        """Test verify_email_async method."""
        request = EmailVerifyAsyncRequest(email="test@example.com")

        with patch('mailersend.resources.email_verification.logger') as mock_logger:
            result = self.resource.verify_email_async(request)

        assert result is self.mock_response
        self.mock_client.request.assert_called_once_with(
            "POST",
            "email-verification/verify-async",
            json={"email": "test@example.com"}
        )
        mock_logger.info.assert_called_once_with("Starting async verification for email: test@example.com")

    def test_get_async_status(self):
        """Test get_async_status method."""
        request = EmailVerificationAsyncStatusRequest(email_verification_id="abc123")

        with patch('mailersend.resources.email_verification.logger') as mock_logger:
            result = self.resource.get_async_status(request)

        assert result is self.mock_response
        self.mock_client.request.assert_called_once_with(
            "GET",
            "email-verification/verify-async/abc123"
        )
        mock_logger.info.assert_called_once_with("Getting async verification status for ID: abc123")

    def test_list_verifications_minimal(self):
        """Test list_verifications with minimal parameters."""
        request = EmailVerificationListsRequest()

        with patch('mailersend.resources.email_verification.logger') as mock_logger:
            result = self.resource.list_verifications(request)

        assert result is self.mock_response
        self.mock_client.request.assert_called_once_with(
            "GET",
            "email-verification",
            params={}
        )
        mock_logger.info.assert_called_once_with("Listing email verification lists")

    def test_list_verifications_with_pagination(self):
        """Test list_verifications with pagination."""
        request = EmailVerificationListsRequest(page=2, limit=50)

        with patch('mailersend.resources.email_verification.logger') as mock_logger:
            result = self.resource.list_verifications(request)

        assert result is self.mock_response
        self.mock_client.request.assert_called_once_with(
            "GET",
            "email-verification",
            params={"page": 2, "limit": 50}
        )
        mock_logger.info.assert_called_once_with("Listing email verification lists")

    def test_get_verification(self):
        """Test get_verification method."""
        request = EmailVerificationGetRequest(email_verification_id="abc123")

        with patch('mailersend.resources.email_verification.logger') as mock_logger:
            result = self.resource.get_verification(request)

        assert result is self.mock_response
        self.mock_client.request.assert_called_once_with(
            "GET",
            "email-verification/abc123"
        )
        mock_logger.info.assert_called_once_with("Getting email verification list: abc123")

    def test_create_verification(self):
        """Test create_verification method."""
        emails = ["test1@example.com", "test2@example.com"]
        request = EmailVerificationCreateRequest(name="Test List", emails=emails)

        with patch('mailersend.resources.email_verification.logger') as mock_logger:
            result = self.resource.create_verification(request)

        assert result is self.mock_response
        self.mock_client.request.assert_called_once_with(
            "POST",
            "email-verification",
            json={"name": "Test List", "emails": emails}
        )
        mock_logger.info.assert_called_once_with("Creating email verification list: Test List with 2 emails")

    def test_verify_list(self):
        """Test verify_list method."""
        request = EmailVerificationVerifyRequest(email_verification_id="abc123")

        with patch('mailersend.resources.email_verification.logger') as mock_logger:
            result = self.resource.verify_list(request)

        assert result is self.mock_response
        self.mock_client.request.assert_called_once_with(
            "GET",
            "email-verification/abc123/verify"
        )
        mock_logger.info.assert_called_once_with("Starting verification for list: abc123")

    def test_get_results_minimal(self):
        """Test get_results with minimal parameters."""
        request = EmailVerificationResultsRequest(email_verification_id="abc123")

        with patch('mailersend.resources.email_verification.logger') as mock_logger:
            result = self.resource.get_results(request)

        assert result is self.mock_response
        self.mock_client.request.assert_called_once_with(
            "GET",
            "email-verification/abc123/results",
            params={}
        )
        mock_logger.info.assert_called_once_with("Getting verification results for list: abc123")

    def test_get_results_with_filters(self):
        """Test get_results with all filters."""
        request = EmailVerificationResultsRequest(
            email_verification_id="abc123",
            page=2,
            limit=25,
            results=["valid", "typo"]
        )

        with patch('mailersend.resources.email_verification.logger') as mock_logger:
            result = self.resource.get_results(request)

        assert result is self.mock_response
        self.mock_client.request.assert_called_once_with(
            "GET",
            "email-verification/abc123/results",
            params={"page": 2, "limit": 25, "results": ["valid", "typo"]}
        )
        mock_logger.info.assert_called_once_with("Getting verification results for list: abc123")

    def test_get_results_empty_results_filter(self):
        """Test get_results with empty results filter."""
        request = EmailVerificationResultsRequest(
            email_verification_id="abc123",
            results=[]
        )

        with patch('mailersend.resources.email_verification.logger') as mock_logger:
            result = self.resource.get_results(request)

        assert result is self.mock_response
        # Empty results list should not be included in params
        self.mock_client.request.assert_called_once_with(
            "GET",
            "email-verification/abc123/results",
            params={}
        )
        mock_logger.info.assert_called_once_with("Getting verification results for list: abc123") 