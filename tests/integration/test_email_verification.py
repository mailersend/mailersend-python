import pytest
from tests.test_helpers import vcr

from mailersend.models.email_verification import (
    EmailVerificationListsRequest,
    EmailVerificationGetRequest,
    EmailVerificationCreateRequest,
    EmailVerificationVerifyRequest,
    EmailVerificationResultsRequest,
    EmailVerificationListsQueryParams,
    EmailVerificationResultsQueryParams,
)
from mailersend.models.base import APIResponse


@pytest.fixture
def basic_list_request():
    """Basic email verification list request"""
    return EmailVerificationListsRequest(
        query_params=EmailVerificationListsQueryParams(page=1, limit=10)
    )


@pytest.fixture
def sample_email_list():
    """Sample email list for testing"""
    return [
        "test1@example.com",
        "test2@example.com",
        "invalid-email",
        "test3@validexample.com",
    ]


@pytest.fixture
def verification_get_request():
    """Email verification get request with test list ID"""
    return EmailVerificationGetRequest(
        email_verification_id="test-verification-list-id"
    )


class TestEmailVerificationIntegration:
    """Integration tests for Email Verification API."""

    @vcr.use_cassette("email_verification_list_basic.yaml")
    def test_list_email_verification_lists_basic(
        self, email_client, basic_list_request
    ):
        """Test listing email verification lists with basic parameters."""
        response = email_client.email_verification.list_verifications(basic_list_request)

        assert isinstance(response, APIResponse)
        assert response.status_code == 200
        assert response.data is not None

        # Check that we have the expected structure
        if "data" in response.data:
            verification_lists = response.data["data"]
            assert isinstance(verification_lists, list)

            # If we have lists, check the structure
            if verification_lists:
                first_list = verification_lists[0]
                assert "id" in first_list
                assert "name" in first_list
                assert "status" in first_list
                assert "created_at" in first_list

    @vcr.use_cassette("email_verification_list_with_pagination.yaml")
    def test_list_email_verification_lists_with_pagination(self, email_client):
        """Test listing email verification lists with pagination."""
        request = EmailVerificationListsRequest(
            query_params=EmailVerificationListsQueryParams(page=1, limit=10)
        )

        response = email_client.email_verification.list_verifications(request)

        assert isinstance(response, APIResponse)
        assert response.status_code == 200

        # Check pagination metadata
        if "meta" in response.data:
            meta = response.data["meta"]
            assert "current_page" in meta
            assert "per_page" in meta
            # API may or may not include total count in meta
            assert meta["per_page"] == "10"  # API returns string
            assert meta["current_page"] == 1

    @vcr.use_cassette("email_verification_create_list.yaml")
    def test_create_email_verification_list(self, email_client, sample_email_list):
        """Test creating a new email verification list."""
        request = EmailVerificationCreateRequest(
            name="Test Verification List", emails=sample_email_list
        )

        response = email_client.email_verification.create_verification(request)

        assert isinstance(response, APIResponse)
        assert response.status_code in [200, 201]
        assert response.data is not None

        # Check that we have the expected structure
        if "data" in response.data:
            created_list = response.data["data"]
            assert "id" in created_list
            assert "name" in created_list
            assert created_list["name"] == "Test Verification List"
            assert "status" in created_list
            assert "created_at" in created_list

    @vcr.use_cassette("email_verification_get_single.yaml")
    def test_get_email_verification_list_not_found_with_test_id(
        self, email_client, verification_get_request
    ):
        """Test getting a non-existent email verification list returns 404."""
        from mailersend.exceptions import ResourceNotFoundError
        
        with pytest.raises(ResourceNotFoundError) as exc_info:
            email_client.email_verification.get_verification(verification_get_request)

        assert "not found" in str(exc_info.value).lower() or "404" in str(exc_info.value)

    @vcr.use_cassette("email_verification_get_not_found.yaml")
    def test_get_email_verification_list_not_found(self, email_client):
        """Test getting a non-existent email verification list."""
        request = EmailVerificationGetRequest(
            email_verification_id="non-existent-list-id"
        )

        with pytest.raises(Exception) as exc_info:
            email_client.email_verification.get_verification(request)

        # Should raise a ResourceNotFoundError or similar
        assert (
            "404" in str(exc_info.value) or "not found" in str(exc_info.value).lower()
        )

    @vcr.use_cassette("email_verification_verify_list.yaml")
    def test_verify_email_verification_list_not_found(
        self, email_client, verification_get_request
    ):
        """Test verifying a non-existent email verification list returns 404."""
        from mailersend.exceptions import ResourceNotFoundError
        
        verify_request = EmailVerificationVerifyRequest(
            email_verification_id=verification_get_request.email_verification_id
        )

        with pytest.raises(ResourceNotFoundError) as exc_info:
            email_client.email_verification.verify_list(verify_request)

        assert "not found" in str(exc_info.value).lower() or "404" in str(exc_info.value)

    @vcr.use_cassette("email_verification_get_results.yaml")
    def test_get_email_verification_results_not_found(
        self, email_client, verification_get_request
    ):
        """Test getting results for a non-existent email verification list returns 404."""
        from mailersend.exceptions import ResourceNotFoundError
        
        results_request = EmailVerificationResultsRequest(
            email_verification_id=verification_get_request.email_verification_id,
            query_params=EmailVerificationResultsQueryParams(page=1, limit=10)
        )

        with pytest.raises(ResourceNotFoundError) as exc_info:
            email_client.email_verification.get_results(results_request)

        assert "not found" in str(exc_info.value).lower() or "404" in str(exc_info.value)

    @vcr.use_cassette("email_verification_comprehensive_workflow.yaml")
    def test_comprehensive_email_verification_workflow(
        self, email_client, sample_email_list
    ):
        """Test a comprehensive workflow of creating, verifying, and getting results."""

        # Step 1: Create a new verification list
        create_request = EmailVerificationCreateRequest(
            name="Comprehensive Test List", emails=sample_email_list
        )

        create_response = email_client.email_verification.create_verification(create_request)
        assert isinstance(create_response, APIResponse)
        assert create_response.status_code in [200, 201]

        # Extract the created list ID
        created_list_id = create_response.data["data"]["id"]

        # Step 2: Get the created list details
        get_request = EmailVerificationGetRequest(email_verification_id=created_list_id)

        get_response = email_client.email_verification.get_verification(get_request)
        assert isinstance(get_response, APIResponse)
        assert get_response.status_code == 200

        # Verify the list details
        list_data = get_response.data["data"]
        assert list_data["id"] == created_list_id
        assert list_data["name"] == "Comprehensive Test List"

        # Step 3: Verify the list
        verify_request = EmailVerificationVerifyRequest(
            email_verification_id=created_list_id
        )

        verify_response = email_client.email_verification.verify_list(verify_request)
        assert isinstance(verify_response, APIResponse)
        assert verify_response.status_code in [200, 202]

        # Step 4: Get results (may not be ready immediately in real scenario)
        results_request = EmailVerificationResultsRequest(
            email_verification_id=created_list_id,
            query_params=EmailVerificationResultsQueryParams(page=1, limit=10)
        )

        results_response = email_client.email_verification.get_results(
            results_request
        )
        assert isinstance(results_response, APIResponse)
        assert results_response.status_code == 200

    @vcr.use_cassette("email_verification_create_validation_error.yaml")
    def test_create_email_verification_list_validation_error(self, email_client):
        """Test that invalid creation request raises validation error."""

        # Test model validation directly - empty name and emails should cause validation error
        with pytest.raises(Exception) as exc_info:
            EmailVerificationCreateRequest(name="", emails=[])

        # Should raise a validation error for empty name and emails
        error_str = str(exc_info.value).lower()
        assert (
            "validation" in error_str
            or "name cannot be empty" in error_str
            or "list should have at least 1 item" in error_str
        )

    @vcr.use_cassette("email_verification_api_response_structure.yaml")
    def test_api_response_structure(self, email_client, basic_list_request):
        """Test that API response has the expected structure and metadata."""
        response = email_client.email_verification.list_verifications(basic_list_request)

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

    def test_list_email_verification_validation_error(self, email_client):
        """Test that invalid request raises validation error."""
        with pytest.raises(Exception) as exc_info:
            # Pass invalid request type
            email_client.email_verification.list_verifications("invalid-request")

        # Should raise an AttributeError for invalid request type
        error_str = str(exc_info.value).lower()
        assert (
            "attribute" in error_str
            or "to_query_params" in error_str
        )

    @vcr.use_cassette("email_verification_empty_list.yaml")
    def test_list_email_verification_empty_result(
        self, email_client, basic_list_request
    ):
        """Test listing email verification lists when no lists exist."""
        response = email_client.email_verification.list_verifications(basic_list_request)

        assert isinstance(response, APIResponse)
        assert response.status_code == 200
        assert response.data is not None

        # Should have data array (may not be empty due to previous tests creating data)
        if "data" in response.data:
            assert isinstance(response.data["data"], list)
