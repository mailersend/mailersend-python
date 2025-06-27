"""Tests for Email Verification API models."""

from datetime import datetime
from typing import List
import pytest
from pydantic import ValidationError

from mailersend.models.email_verification import (
    # Request models
    EmailVerifyRequest,
    EmailVerifyAsyncRequest,
    EmailVerificationAsyncStatusRequest,
    EmailVerificationListsRequest,
    EmailVerificationGetRequest,
    EmailVerificationCreateRequest,
    EmailVerificationVerifyRequest,
    EmailVerificationResultsRequest,
    # Response models
    EmailVerifyResponse,
    EmailVerifyAsyncResponse,
    EmailVerificationAsyncStatusResponse,
    EmailVerificationStatus,
    EmailVerificationStatistics,
    EmailVerification,
    EmailVerificationListsResponse,
    EmailVerificationResponse,
    EmailVerificationResult,
    EmailVerificationResultsResponse,
    EmailVerificationLinks,
    EmailVerificationMeta,
)


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

    def test_valid_request_minimal(self):
        """Test creating a valid minimal lists request."""
        request = EmailVerificationListsRequest()
        assert request.page is None
        assert request.limit is None

    def test_valid_request_with_pagination(self):
        """Test creating a valid lists request with pagination."""
        request = EmailVerificationListsRequest(page=2, limit=50)
        assert request.page == 2
        assert request.limit == 50

    def test_invalid_page_validation(self):
        """Test validation fails for invalid page."""
        with pytest.raises(ValidationError) as excinfo:
            EmailVerificationListsRequest(page=0)
        assert "greater than or equal to 1" in str(excinfo.value)

    def test_invalid_limit_too_low(self):
        """Test validation fails for limit too low."""
        with pytest.raises(ValidationError) as excinfo:
            EmailVerificationListsRequest(limit=5)
        assert "greater than or equal to 10" in str(excinfo.value)

    def test_invalid_limit_too_high(self):
        """Test validation fails for limit too high."""
        with pytest.raises(ValidationError) as excinfo:
            EmailVerificationListsRequest(limit=150)
        assert "less than or equal to 100" in str(excinfo.value)


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
            name="  Test List  ",
            emails=["  test1@example.com  ", "test2@example.com"]
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

    def test_valid_request_minimal(self):
        """Test creating a valid minimal results request."""
        request = EmailVerificationResultsRequest(email_verification_id="abc123")
        assert request.email_verification_id == "abc123"
        assert request.page is None
        assert request.limit is None
        assert request.results is None

    def test_valid_request_with_filters(self):
        """Test creating a valid results request with filters."""
        request = EmailVerificationResultsRequest(
            email_verification_id="abc123",
            page=2,
            limit=25,
            results=["valid", "typo"]
        )
        assert request.email_verification_id == "abc123"
        assert request.page == 2
        assert request.limit == 25
        assert request.results == ["valid", "typo"]

    def test_invalid_result_filter_validation(self):
        """Test validation fails for invalid result filter."""
        with pytest.raises(ValidationError) as excinfo:
            EmailVerificationResultsRequest(
                email_verification_id="abc123",
                results=["valid", "invalid_result"]
            )
        assert "Invalid result filter: invalid_result" in str(excinfo.value)


class TestEmailVerifyResponse:
    """Test EmailVerifyResponse model."""

    def test_valid_response(self):
        """Test creating a valid verify response."""
        response = EmailVerifyResponse(status="valid")
        assert response.status == "valid"


class TestEmailVerifyAsyncResponse:
    """Test EmailVerifyAsyncResponse model."""

    def test_valid_response(self):
        """Test creating a valid async verify response."""
        response = EmailVerifyAsyncResponse(
            id="abc123",
            address="test@example.com",
            status="queued",
            result=None,
            error=None
        )
        assert response.id == "abc123"
        assert response.address == "test@example.com"
        assert response.status == "queued"
        assert response.result is None
        assert response.error is None


class TestEmailVerificationAsyncStatusResponse:
    """Test EmailVerificationAsyncStatusResponse model."""

    def test_valid_response(self):
        """Test creating a valid async status response."""
        response = EmailVerificationAsyncStatusResponse(
            id="abc123",
            address="test@example.com",
            status="completed",
            result="valid",
            error=None
        )
        assert response.id == "abc123"
        assert response.address == "test@example.com"
        assert response.status == "completed"
        assert response.result == "valid"
        assert response.error is None


class TestEmailVerificationStatus:
    """Test EmailVerificationStatus model."""

    def test_valid_status(self):
        """Test creating a valid verification status."""
        status = EmailVerificationStatus(name="verifying", count=5)
        assert status.name == "verifying"
        assert status.count == 5


class TestEmailVerificationStatistics:
    """Test EmailVerificationStatistics model."""

    def test_valid_statistics(self):
        """Test creating valid verification statistics."""
        stats = EmailVerificationStatistics(
            valid=10,
            catch_all=2,
            mailbox_full=1,
            role_based=3,
            unknown=5,
            syntax_error=2,
            typo=1,
            mailbox_not_found=4,
            disposable=0,
            mailbox_blocked=1,
            failed=0
        )
        assert stats.valid == 10
        assert stats.catch_all == 2
        assert stats.mailbox_full == 1
        assert stats.role_based == 3
        assert stats.unknown == 5
        assert stats.syntax_error == 2
        assert stats.typo == 1
        assert stats.mailbox_not_found == 4
        assert stats.disposable == 0
        assert stats.mailbox_blocked == 1
        assert stats.failed == 0


class TestEmailVerification:
    """Test EmailVerification model."""

    def test_valid_verification(self):
        """Test creating a valid email verification."""
        now = datetime.now()
        status = EmailVerificationStatus(name="verified", count=100)
        stats = EmailVerificationStatistics(
            valid=80, catch_all=5, mailbox_full=2, role_based=3, unknown=5,
            syntax_error=1, typo=2, mailbox_not_found=1, disposable=1, 
            mailbox_blocked=0, failed=0
        )
        
        verification = EmailVerification(
            id="abc123",
            name="Test List",
            total=100,
            verification_started=now,
            verification_ended=now,
            created_at=now,
            updated_at=now,
            status=status,
            source="api",
            statistics=stats
        )
        
        assert verification.id == "abc123"
        assert verification.name == "Test List"
        assert verification.total == 100
        assert verification.verification_started == now
        assert verification.verification_ended == now
        assert verification.created_at == now
        assert verification.updated_at == now
        assert verification.status == status
        assert verification.source == "api"
        assert verification.statistics == stats


class TestEmailVerificationLinks:
    """Test EmailVerificationLinks model."""

    def test_valid_links(self):
        """Test creating valid pagination links."""
        links = EmailVerificationLinks(
            first="http://example.com?page=1",
            last="http://example.com?page=10",
            prev=None,
            next="http://example.com?page=3"
        )
        assert links.first == "http://example.com?page=1"
        assert links.last == "http://example.com?page=10"
        assert links.prev is None
        assert links.next == "http://example.com?page=3"


class TestEmailVerificationMeta:
    """Test EmailVerificationMeta model."""

    def test_valid_meta(self):
        """Test creating valid pagination metadata."""
        meta = EmailVerificationMeta(
            current_page=2,
            **{"from": 26},  # Use dict unpacking to pass the "from" field
            path="http://example.com/email-verification",
            per_page="25",
            to=50
        )
        assert meta.current_page == 2
        assert meta.from_ == 26
        assert meta.path == "http://example.com/email-verification"
        assert meta.per_page == "25"
        assert meta.to == 50


class TestEmailVerificationListsResponse:
    """Test EmailVerificationListsResponse model."""

    def test_valid_response(self):
        """Test creating a valid lists response."""
        now = datetime.now()
        status = EmailVerificationStatus(name="verified", count=100)
        stats = EmailVerificationStatistics(
            valid=80, catch_all=5, mailbox_full=2, role_based=3, unknown=5,
            syntax_error=1, typo=2, mailbox_not_found=1, disposable=1, 
            mailbox_blocked=0, failed=0
        )
        verification = EmailVerification(
            id="abc123", name="Test List", total=100,
            verification_started=now, verification_ended=now,
            created_at=now, updated_at=now,
            status=status, source="api", statistics=stats
        )
        links = EmailVerificationLinks(first="http://example.com?page=1")
        meta = EmailVerificationMeta(
            current_page=1, from_=1, path="http://example.com", per_page="25", to=1
        )
        
        response = EmailVerificationListsResponse(
            data=[verification],
            links=links,
            meta=meta
        )
        
        assert len(response.data) == 1
        assert response.data[0] == verification
        assert response.links == links
        assert response.meta == meta


class TestEmailVerificationResponse:
    """Test EmailVerificationResponse model."""

    def test_valid_response(self):
        """Test creating a valid verification response."""
        now = datetime.now()
        status = EmailVerificationStatus(name="verified", count=100)
        stats = EmailVerificationStatistics(
            valid=80, catch_all=5, mailbox_full=2, role_based=3, unknown=5,
            syntax_error=1, typo=2, mailbox_not_found=1, disposable=1, 
            mailbox_blocked=0, failed=0
        )
        verification = EmailVerification(
            id="abc123", name="Test List", total=100,
            verification_started=now, verification_ended=now,
            created_at=now, updated_at=now,
            status=status, source="api", statistics=stats
        )
        
        response = EmailVerificationResponse(data=verification)
        assert response.data == verification


class TestEmailVerificationResult:
    """Test EmailVerificationResult model."""

    def test_valid_result(self):
        """Test creating a valid verification result."""
        result = EmailVerificationResult(
            address="test@example.com",
            result="valid"
        )
        assert result.address == "test@example.com"
        assert result.result == "valid"


class TestEmailVerificationResultsResponse:
    """Test EmailVerificationResultsResponse model."""

    def test_valid_response(self):
        """Test creating a valid results response."""
        results = [
            EmailVerificationResult(address="test1@example.com", result="valid"),
            EmailVerificationResult(address="test2@example.com", result="typo")
        ]
        links = EmailVerificationLinks(first="http://example.com?page=1")
        meta = EmailVerificationMeta(
            current_page=1, from_=1, path="http://example.com", per_page="25", to=2
        )
        
        response = EmailVerificationResultsResponse(
            data=results,
            links=links,
            meta=meta
        )
        
        assert len(response.data) == 2
        assert response.data[0].address == "test1@example.com"
        assert response.data[1].result == "typo"
        assert response.links == links
        assert response.meta == meta 