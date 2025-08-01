"""Tests for Email Verification API models."""

from datetime import datetime
from typing import List
import pytest
from pydantic import ValidationError

from mailersend.models.email_verification import (
    # Query params models
    EmailVerificationListsQueryParams,
    EmailVerificationResultsQueryParams,
    # Request models
    EmailVerifyRequest,
    EmailVerifyAsyncRequest,
    EmailVerificationAsyncStatusRequest,
    EmailVerificationListsRequest,
    EmailVerificationGetRequest,
    EmailVerificationCreateRequest,
    EmailVerificationVerifyRequest,
    EmailVerificationResultsRequest,
)


class TestEmailVerificationListsQueryParams:
    """Test EmailVerificationListsQueryParams model."""

    def test_default_values(self):
        """Test query params with default values."""
        params = EmailVerificationListsQueryParams()
        assert params.page == 1
        assert params.limit == 25

    def test_custom_values(self):
        """Test query params with custom values."""
        params = EmailVerificationListsQueryParams(page=2, limit=50)
        assert params.page == 2
        assert params.limit == 50

    def test_invalid_page_validation(self):
        """Test validation fails for invalid page."""
        with pytest.raises(ValidationError) as excinfo:
            EmailVerificationListsQueryParams(page=0)
        assert "greater than or equal to 1" in str(excinfo.value)

    def test_invalid_limit_too_low(self):
        """Test validation fails for limit too low."""
        with pytest.raises(ValidationError) as excinfo:
            EmailVerificationListsQueryParams(limit=5)
        assert "greater than or equal to 10" in str(excinfo.value)

    def test_invalid_limit_too_high(self):
        """Test validation fails for limit too high."""
        with pytest.raises(ValidationError) as excinfo:
            EmailVerificationListsQueryParams(limit=150)
        assert "less than or equal to 100" in str(excinfo.value)

    def test_to_query_params(self):
        """Test converting to query parameters."""
        params = EmailVerificationListsQueryParams(page=2, limit=50)
        query_params = params.to_query_params()
        assert query_params == {"page": 2, "limit": 50}


class TestEmailVerificationResultsQueryParams:
    """Test EmailVerificationResultsQueryParams model."""

    def test_default_values(self):
        """Test query params with default values."""
        params = EmailVerificationResultsQueryParams()
        assert params.page == 1
        assert params.limit == 25
        assert params.results is None

    def test_custom_values(self):
        """Test query params with custom values."""
        results = ["valid", "catch_all"]
        params = EmailVerificationResultsQueryParams(page=2, limit=50, results=results)
        assert params.page == 2
        assert params.limit == 50
        assert params.results == results

    def test_valid_results_filter(self):
        """Test valid results filter values."""
        valid_results = [
            "valid",
            "catch_all",
            "mailbox_full",
            "role_based",
            "unknown",
            "failed",
        ]
        params = EmailVerificationResultsQueryParams(results=valid_results)
        assert params.results == valid_results

    def test_invalid_result_filter_validation(self):
        """Test validation fails for invalid result filter."""
        with pytest.raises(ValidationError) as excinfo:
            EmailVerificationResultsQueryParams(results=["invalid_result"])
        assert "Invalid result filter: invalid_result" in str(excinfo.value)

    def test_to_query_params_with_results(self):
        """Test converting to query parameters with results filter."""
        results = ["valid", "catch_all"]
        params = EmailVerificationResultsQueryParams(page=2, limit=50, results=results)
        query_params = params.to_query_params()
        assert query_params == {"page": 2, "limit": 50, "results": results}

    def test_to_query_params_without_results(self):
        """Test converting to query parameters without results filter."""
        params = EmailVerificationResultsQueryParams(page=2, limit=50)
        query_params = params.to_query_params()
        assert query_params == {"page": 2, "limit": 50}


class TestEmailVerifyRequest:
    """Test EmailVerifyRequest model."""

    def test_valid_request(self):
        """Test creating a valid email verify request."""
        request = EmailVerifyRequest(email="test@example.com")
        assert request.email == "test@example.com"

    def test_empty_email_validation(self):
        """Test validation fails for empty email."""
        with pytest.raises(ValidationError) as excinfo:
            EmailVerifyRequest(email="")
        assert "email cannot be empty" in str(excinfo.value)

    def test_whitespace_email_validation(self):
        """Test validation fails for whitespace-only email."""
        with pytest.raises(ValidationError) as excinfo:
            EmailVerifyRequest(email="   ")
        assert "email cannot be empty" in str(excinfo.value)

    def test_email_trimming(self):
        """Test that email gets trimmed."""
        request = EmailVerifyRequest(email="  test@example.com  ")
        assert request.email == "test@example.com"


class TestEmailVerifyAsyncRequest:
    """Test EmailVerifyAsyncRequest model."""

    def test_valid_request(self):
        """Test creating a valid async email verify request."""
        request = EmailVerifyAsyncRequest(email="test@example.com")
        assert request.email == "test@example.com"

    def test_empty_email_validation(self):
        """Test validation fails for empty email."""
        with pytest.raises(ValidationError) as excinfo:
            EmailVerifyAsyncRequest(email="")
        assert "email cannot be empty" in str(excinfo.value)


class TestEmailVerificationAsyncStatusRequest:
    """Test EmailVerificationAsyncStatusRequest model."""

    def test_valid_request(self):
        """Test creating a valid async status request."""
        request = EmailVerificationAsyncStatusRequest(email_verification_id="abc123")
        assert request.email_verification_id == "abc123"

    def test_empty_id_validation(self):
        """Test validation fails for empty ID."""
        with pytest.raises(ValidationError) as excinfo:
            EmailVerificationAsyncStatusRequest(email_verification_id="")
        assert "email_verification_id cannot be empty" in str(excinfo.value)


class TestEmailVerificationListsRequest:
    """Test EmailVerificationListsRequest model."""

    def test_valid_request_with_defaults(self):
        """Test creating a valid lists request with defaults."""
        query_params = EmailVerificationListsQueryParams()
        request = EmailVerificationListsRequest(query_params=query_params)

        params = request.to_query_params()
        assert params == {"page": 1, "limit": 25}

    def test_valid_request_with_custom_params(self):
        """Test creating a valid lists request with custom parameters."""
        query_params = EmailVerificationListsQueryParams(page=2, limit=50)
        request = EmailVerificationListsRequest(query_params=query_params)

        params = request.to_query_params()
        assert params == {"page": 2, "limit": 50}


class TestEmailVerificationGetRequest:
    """Test EmailVerificationGetRequest model."""

    def test_valid_request(self):
        """Test creating a valid get request."""
        request = EmailVerificationGetRequest(email_verification_id="abc123")
        assert request.email_verification_id == "abc123"

    def test_empty_id_validation(self):
        """Test validation fails for empty ID."""
        with pytest.raises(ValidationError) as excinfo:
            EmailVerificationGetRequest(email_verification_id="")
        assert "email_verification_id cannot be empty" in str(excinfo.value)


class TestEmailVerificationCreateRequest:
    """Test EmailVerificationCreateRequest model."""

    def test_valid_request(self):
        """Test creating a valid create request."""
        emails = ["test1@example.com", "test2@example.com"]
        request = EmailVerificationCreateRequest(name="Test List", emails=emails)
        assert request.name == "Test List"
        assert request.emails == emails

    def test_empty_name_validation(self):
        """Test validation fails for empty name."""
        with pytest.raises(ValidationError) as excinfo:
            EmailVerificationCreateRequest(name="", emails=["test@example.com"])
        assert "name cannot be empty" in str(excinfo.value)

    def test_empty_emails_validation(self):
        """Test validation fails for empty emails list."""
        with pytest.raises(ValidationError) as excinfo:
            EmailVerificationCreateRequest(name="Test", emails=[])
        assert "at least 1 item" in str(excinfo.value)

    def test_empty_email_in_list_validation(self):
        """Test validation fails for empty email in list."""
        with pytest.raises(ValidationError) as excinfo:
            EmailVerificationCreateRequest(name="Test", emails=["test@example.com", ""])
        assert "email addresses cannot be empty" in str(excinfo.value)

    def test_email_too_long_validation(self):
        """Test validation fails for email too long."""
        long_email = "a" * 192 + "@example.com"
        with pytest.raises(ValidationError) as excinfo:
            EmailVerificationCreateRequest(name="Test", emails=[long_email])
        assert "email addresses cannot exceed 191 characters" in str(excinfo.value)

    def test_email_trimming(self):
        """Test that emails get trimmed."""
        request = EmailVerificationCreateRequest(
            name="  Test List  ", emails=["  test1@example.com  ", "test2@example.com"]
        )
        assert request.name == "Test List"
        assert request.emails == ["test1@example.com", "test2@example.com"]


class TestEmailVerificationVerifyRequest:
    """Test EmailVerificationVerifyRequest model."""

    def test_valid_request(self):
        """Test creating a valid verify request."""
        request = EmailVerificationVerifyRequest(email_verification_id="abc123")
        assert request.email_verification_id == "abc123"

    def test_empty_id_validation(self):
        """Test validation fails for empty ID."""
        with pytest.raises(ValidationError) as excinfo:
            EmailVerificationVerifyRequest(email_verification_id="")
        assert "email_verification_id cannot be empty" in str(excinfo.value)


class TestEmailVerificationResultsRequest:
    """Test EmailVerificationResultsRequest model."""

    def test_valid_request_with_defaults(self):
        """Test creating a valid results request with defaults."""
        query_params = EmailVerificationResultsQueryParams()
        request = EmailVerificationResultsRequest(
            email_verification_id="abc123", query_params=query_params
        )
        assert request.email_verification_id == "abc123"

        params = request.to_query_params()
        assert params == {"page": 1, "limit": 25}

    def test_valid_request_with_filters(self):
        """Test creating a valid results request with filters."""
        results = ["valid", "catch_all"]
        query_params = EmailVerificationResultsQueryParams(
            page=2, limit=50, results=results
        )
        request = EmailVerificationResultsRequest(
            email_verification_id="abc123", query_params=query_params
        )
        assert request.email_verification_id == "abc123"

        params = request.to_query_params()
        assert params == {"page": 2, "limit": 50, "results": results}

    def test_empty_id_validation(self):
        """Test validation fails for empty verification ID."""
        query_params = EmailVerificationResultsQueryParams()
        with pytest.raises(ValidationError) as excinfo:
            EmailVerificationResultsRequest(
                email_verification_id="", query_params=query_params
            )
        assert "email_verification_id cannot be empty" in str(excinfo.value)
