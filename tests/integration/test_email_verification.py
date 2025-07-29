import pytest
from tests.test_helpers import vcr

from mailersend.models.email_verification import (
    EmailVerificationListsRequest,
    EmailVerificationGetRequest,
    EmailVerificationCreateRequest,
    EmailVerificationVerifyRequest,
    EmailVerificationResultsRequest,
    EmailVerificationListsQueryParams,
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
        response = email_client.email_verification.get_all_lists(basic_list_request)

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
        request = EmailVerificationListRequest(
            query_params=EmailVerificationQueryParams(page=1, limit=5)
        )

        response = email_client.email_verification.get_all_lists(request)

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

    @vcr.use_cassette("email_verification_create_list.yaml")
    def test_create_email_verification_list(self, email_client, sample_email_list):
        """Test creating a new email verification list."""
        request = EmailVerificationCreateRequest(
            name="Test Verification List", emails=sample_email_list
        )

        response = email_client.email_verification.create_list(request)

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
    def test_get_email_verification_list_success(
        self, email_client, verification_get_request
    ):
        """Test getting a single email verification list successfully."""
        response = email_client.email_verification.get_list(verification_get_request)

        assert isinstance(response, APIResponse)
        assert response.status_code == 200
        assert response.data is not None

        # Check that we have the expected structure
        if "data" in response.data:
            verification_list = response.data["data"]
            assert "id" in verification_list
            assert "name" in verification_list
            assert "status" in verification_list
            assert "created_at" in verification_list
            assert "updated_at" in verification_list

            # Verify the ID matches what we requested
            assert (
                verification_list["id"]
                == verification_get_request.email_verification_id
            )

    @vcr.use_cassette("email_verification_get_not_found.yaml")
    def test_get_email_verification_list_not_found(self, email_client):
        """Test getting a non-existent email verification list."""
        request = EmailVerificationGetRequest(
            email_verification_id="non-existent-list-id"
        )

        with pytest.raises(Exception) as exc_info:
            email_client.email_verification.get_list(request)

        # Should raise a ResourceNotFoundError or similar
        assert (
            "404" in str(exc_info.value) or "not found" in str(exc_info.value).lower()
        )

    @vcr.use_cassette("email_verification_verify_list.yaml")
    def test_verify_email_verification_list(
        self, email_client, verification_get_request
    ):
        """Test verifying an email verification list."""
        verify_request = EmailVerificationVerifyRequest(
            email_verification_id=verification_get_request.email_verification_id
        )

        response = email_client.email_verification.verify_list(verify_request)

        assert isinstance(response, APIResponse)
        assert response.status_code in [200, 202]  # 202 for async processing
        assert response.data is not None

        # The response should indicate verification has started
        if "data" in response.data:
            verification_data = response.data["data"]
            assert "id" in verification_data
            # Status should be 'processing' or 'verified'
            if "status" in verification_data:
                assert verification_data["status"] in [
                    "processing",
                    "verified",
                    "pending",
                ]

    @vcr.use_cassette("email_verification_get_results.yaml")
    def test_get_email_verification_results(
        self, email_client, verification_get_request
    ):
        """Test getting email verification results."""
        results_request = EmailVerificationResultsRequest(
            email_verification_id=verification_get_request.email_verification_id
        )

        response = email_client.email_verification.get_list_results(results_request)

        assert isinstance(response, APIResponse)
        assert response.status_code == 200
        assert response.data is not None

        # Check that we have the expected results structure
        if "data" in response.data:
            results = response.data["data"]
            assert isinstance(results, list)

            # If we have results, check the structure
            if results:
                first_result = results[0]
                assert "email" in first_result
                assert "result" in first_result
                assert "reason" in first_result

                # Result should be one of the valid statuses
                valid_results = ["valid", "invalid", "unknown", "risky"]
                assert first_result["result"] in valid_results

    @vcr.use_cassette("email_verification_comprehensive_workflow.yaml")
    def test_comprehensive_email_verification_workflow(
        self, email_client, sample_email_list
    ):
        """Test a comprehensive workflow of creating, verifying, and getting results."""

        # Step 1: Create a new verification list
        create_request = EmailVerificationCreateRequest(
            name="Comprehensive Test List", emails=sample_email_list
        )

        create_response = email_client.email_verification.create_list(create_request)
        assert isinstance(create_response, APIResponse)
        assert create_response.status_code in [200, 201]

        # Extract the created list ID
        created_list_id = create_response.data["data"]["id"]

        # Step 2: Get the created list details
        get_request = EmailVerificationGetRequest(email_verification_id=created_list_id)

        get_response = email_client.email_verification.get_list(get_request)
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
            email_verification_id=created_list_id
        )

        results_response = email_client.email_verification.get_list_results(
            results_request
        )
        assert isinstance(results_response, APIResponse)
        assert results_response.status_code == 200

    @vcr.use_cassette("email_verification_create_validation_error.yaml")
    def test_create_email_verification_list_validation_error(self, email_client):
        """Test that invalid creation request raises validation error."""

        # Empty name should cause validation error
        request = EmailVerificationCreateRequest(name="", emails=[])

        with pytest.raises(Exception) as exc_info:
            email_client.email_verification.create_list(request)

        # Should raise a validation error
        assert (
            "validation" in str(exc_info.value).lower()
            or "invalid" in str(exc_info.value).lower()
        )

    @vcr.use_cassette("email_verification_api_response_structure.yaml")
    def test_api_response_structure(self, email_client, basic_list_request):
        """Test that API response has the expected structure and metadata."""
        response = email_client.email_verification.get_all_lists(basic_list_request)

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

    def test_list_email_verification_validation_error(self, email_client):
        """Test that invalid request raises validation error."""
        with pytest.raises(Exception) as exc_info:
            # Pass invalid request type
            email_client.email_verification.get_all_lists("invalid-request")

        # Should raise a validation error
        assert (
            "validation" in str(exc_info.value).lower()
            or "invalid" in str(exc_info.value).lower()
        )

    @vcr.use_cassette("email_verification_empty_list.yaml")
    def test_list_email_verification_empty_result(
        self, email_client, basic_list_request
    ):
        """Test listing email verification lists when no lists exist."""
        response = email_client.email_verification.get_all_lists(basic_list_request)

        assert isinstance(response, APIResponse)
        assert response.status_code == 200
        assert response.data is not None

        # Should have empty data array
        if "data" in response.data:
            assert response.data["data"] == []
