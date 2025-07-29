"""Tests for Email Verification API resource."""

from mailersend.resources.email_verification import EmailVerification
from mailersend.models.base import APIResponse
from mailersend.models.email_verification import (
    EmailVerificationListsQueryParams,
    EmailVerificationResultsQueryParams,
    EmailVerifyRequest,
    EmailVerifyAsyncRequest,
    EmailVerificationAsyncStatusRequest,
    EmailVerificationListsRequest,
    EmailVerificationGetRequest,
    EmailVerificationCreateRequest,
    EmailVerificationVerifyRequest,
    EmailVerificationResultsRequest,
)
from unittest.mock import Mock


class TestEmailVerification:
    """Test EmailVerification resource class."""

    def setup_method(self):
        """Set up test fixtures."""
        self.mock_client = Mock()
        self.resource = EmailVerification(self.mock_client)
        self.mock_response = Mock()
        self.mock_response.json.return_value = {"status": "completed"}
        self.mock_response.headers = {"x-request-id": "test-request-id"}
        self.mock_response.status_code = 200
        self.mock_client.request.return_value = self.mock_response

    def test_verify_email_valid_request(self):
        """Test verify_email with valid request."""
        request = EmailVerifyRequest(email="test@example.com")

        result = self.resource.verify_email(request)

        assert isinstance(result, APIResponse)
        self.mock_client.request.assert_called_once_with(
            "POST",
            "email-verification/verify",
            body={"email": "test@example.com"}
        )

    def test_verify_email_async_valid_request(self):
        """Test verify_email_async with valid request."""
        request = EmailVerifyAsyncRequest(email="test@example.com")
        self.mock_response.json.return_value = {
            "id": "abc123",
            "address": "test@example.com",
            "status": "processing"
        }

        result = self.resource.verify_email_async(request)

        assert isinstance(result, APIResponse)
        self.mock_client.request.assert_called_once_with(
            "POST",
            "email-verification/verify-async",
            body={"email": "test@example.com"}
        )

    def test_get_async_status_valid_request(self):
        """Test get_async_status with valid request."""
        request = EmailVerificationAsyncStatusRequest(email_verification_id="abc123")
        self.mock_response.json.return_value = {
            "id": "abc123",
            "address": "test@example.com",
            "status": "completed"
        }

        result = self.resource.get_async_status(request)

        assert isinstance(result, APIResponse)
        self.mock_client.request.assert_called_once_with(
            method="GET", 
            endpoint="email-verification/verify-async/abc123"
        )

    def test_list_verifications_with_defaults(self):
        """Test list_verifications with default parameters."""
        query_params = EmailVerificationListsQueryParams()
        request = EmailVerificationListsRequest(query_params=query_params)
        self.mock_response.json.return_value = {
            "data": [],
            "links": {
                "first": "https://api.mailersend.com/v1/email-verification?page=1",
                "last": "https://api.mailersend.com/v1/email-verification?page=1",
                "prev": None,
                "next": None
            },
            "meta": {
                "current_page": 1,
                "from": None,
                "path": "email-verification",
                "per_page": "25",
                "to": None
            }
        }

        result = self.resource.list_verifications(request)

        assert isinstance(result, APIResponse)
        self.mock_client.request.assert_called_once_with(
            method="GET",
            endpoint="email-verification",
            params={"page": 1, "limit": 25}
        )

    def test_list_verifications_with_custom_params(self):
        """Test list_verifications with custom parameters."""
        query_params = EmailVerificationListsQueryParams(page=2, limit=50)
        request = EmailVerificationListsRequest(query_params=query_params)
        self.mock_response.json.return_value = {
            "data": [],
            "links": {
                "first": "https://api.mailersend.com/v1/email-verification?page=1",
                "last": "https://api.mailersend.com/v1/email-verification?page=2",
                "prev": "https://api.mailersend.com/v1/email-verification?page=1",
                "next": None
            },
            "meta": {
                "current_page": 2,
                "from": 51,
                "path": "email-verification",
                "per_page": "50",
                "to": 100
            }
        }

        result = self.resource.list_verifications(request)

        assert isinstance(result, APIResponse)
        self.mock_client.request.assert_called_once_with(
            method="GET",
            endpoint="email-verification",
            params={"page": 2, "limit": 50}
        )

    def test_get_verification_valid_request(self):
        """Test get_verification with valid request."""
        request = EmailVerificationGetRequest(email_verification_id="abc123")
        self.mock_response.json.return_value = {
            "data": {
                "id": "abc123",
                "name": "Test List",
                "total": 100,
                "created_at": "2023-01-01T10:00:00Z",
                "updated_at": "2023-01-01T11:00:00Z",
                "status": {"name": "completed", "count": 100},
                "source": "api",
                "statistics": {
                    "valid": 50, "catch_all": 10, "mailbox_full": 5,
                    "role_based": 8, "unknown": 2, "syntax_error": 3,
                    "typo": 1, "mailbox_not_found": 7, "disposable": 4,
                    "mailbox_blocked": 6, "failed": 4
                }
            }
        }

        result = self.resource.get_verification(request)

        assert isinstance(result, APIResponse)
        self.mock_client.request.assert_called_once_with(
            method="GET",
            endpoint="email-verification/abc123"
        )

    def test_create_verification_valid_request(self):
        """Test create_verification with valid request."""
        emails = ["test1@example.com", "test2@example.com"]
        request = EmailVerificationCreateRequest(name="Test List", emails=emails)
        self.mock_response.json.return_value = {
            "data": {
                "id": "abc123",
                "name": "Test List",
                "total": 2,
                "created_at": "2023-01-01T10:00:00Z",
                "updated_at": "2023-01-01T10:00:00Z",
                "status": {"name": "pending", "count": 0},
                "source": "api",
                "statistics": {
                    "valid": 0, "catch_all": 0, "mailbox_full": 0,
                    "role_based": 0, "unknown": 0, "syntax_error": 0,
                    "typo": 0, "mailbox_not_found": 0, "disposable": 0,
                    "mailbox_blocked": 0, "failed": 0
                }
            }
        }

        result = self.resource.create_verification(request)

        assert isinstance(result, APIResponse)
        self.mock_client.request.assert_called_once_with(
            "POST",
            "email-verification",
            body={"name": "Test List", "emails": emails}
        )

    def test_verify_list_valid_request(self):
        """Test verify_list with valid request."""
        request = EmailVerificationVerifyRequest(email_verification_id="abc123")
        self.mock_response.json.return_value = {
            "data": {
                "id": "abc123",
                "name": "Test List",
                "total": 100,
                "created_at": "2023-01-01T10:00:00Z",
                "updated_at": "2023-01-01T11:00:00Z",
                "status": {"name": "verifying", "count": 0},
                "source": "api",
                "statistics": {
                    "valid": 0, "catch_all": 0, "mailbox_full": 0,
                    "role_based": 0, "unknown": 0, "syntax_error": 0,
                    "typo": 0, "mailbox_not_found": 0, "disposable": 0,
                    "mailbox_blocked": 0, "failed": 0
                }
            }
        }

        result = self.resource.verify_list(request)

        assert isinstance(result, APIResponse)
        self.mock_client.request.assert_called_once_with(
            method="GET",
            endpoint="email-verification/abc123/verify"
        )

    def test_get_results_with_defaults(self):
        """Test get_results with default parameters."""
        query_params = EmailVerificationResultsQueryParams()
        request = EmailVerificationResultsRequest(
            email_verification_id="abc123",
            query_params=query_params
        )
        self.mock_response.json.return_value = {
            "data": [],
            "links": {
                "first": "https://api.mailersend.com/v1/email-verification/abc123/results?page=1",
                "last": "https://api.mailersend.com/v1/email-verification/abc123/results?page=1",
                "prev": None,
                "next": None
            },
            "meta": {
                "current_page": 1,
                "from": None,
                "path": "email-verification/abc123/results",
                "per_page": "25",
                "to": None
            }
        }

        result = self.resource.get_results(request)

        assert isinstance(result, APIResponse)
        self.mock_client.request.assert_called_once_with(
            method="GET",
            endpoint="email-verification/abc123/results",
            params={"page": 1, "limit": 25}
        )

    def test_get_results_with_filters(self):
        """Test get_results with filters."""
        results_filter = ["valid", "catch_all"]
        query_params = EmailVerificationResultsQueryParams(
            page=2, limit=50, results=results_filter
        )
        request = EmailVerificationResultsRequest(
            email_verification_id="abc123",
            query_params=query_params
        )
        self.mock_response.json.return_value = {
            "data": [],
            "links": {
                "first": "https://api.mailersend.com/v1/email-verification/abc123/results?page=1",
                "last": "https://api.mailersend.com/v1/email-verification/abc123/results?page=2",
                "prev": "https://api.mailersend.com/v1/email-verification/abc123/results?page=1",
                "next": None
            },
            "meta": {
                "current_page": 2,
                "from": 51,
                "path": "email-verification/abc123/results",
                "per_page": "50",
                "to": 100
            }
        }

        result = self.resource.get_results(request)

        assert isinstance(result, APIResponse)
        self.mock_client.request.assert_called_once_with(
            method="GET",
            endpoint="email-verification/abc123/results",
            params={"page": 2, "limit": 50, "results": results_filter}
        ) 