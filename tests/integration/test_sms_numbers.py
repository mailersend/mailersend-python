import pytest
from tests.test_helpers import vcr, email_client
import os

from mailersend.models.sms_numbers import (
    SmsNumbersListRequest,
    SmsNumberGetRequest,
    SmsNumberUpdateRequest,
    SmsNumberDeleteRequest,
)
from mailersend.models.base import APIResponse


@pytest.fixture
def basic_sms_numbers_list_request():
    """Basic SMS numbers list request"""
    return SmsNumbersListRequest()


@pytest.fixture
def sms_numbers_list_request_with_filters():
    """SMS numbers list request with filters"""
    return SmsNumbersListRequest(
        paused=False,
        page=1,
        limit=10
    )


@pytest.fixture
def sms_number_get_request():
    """SMS number get request with test SMS number ID"""
    return SmsNumberGetRequest(sms_number_id="test-sms-number-id")


@pytest.fixture
def sms_number_id_from_env():
    """Get SMS number ID from environment or use test ID"""
    return os.environ.get("SDK_SMS_NUMBER_ID", "test-sms-number-id")


@pytest.fixture
def sms_number_update_request(sms_number_id_from_env):
    """SMS number update request"""
    return SmsNumberUpdateRequest(
        sms_number_id=sms_number_id_from_env,
        paused=True
    )


@pytest.fixture
def sms_number_delete_request(sms_number_id_from_env):
    """SMS number delete request"""
    return SmsNumberDeleteRequest(sms_number_id=sms_number_id_from_env)


class TestSmsNumbersIntegration:
    """Integration tests for SMS Numbers API."""

    # ============================================================================
    # SMS Numbers List Tests
    # ============================================================================

    @vcr.use_cassette("sms_numbers_list_basic.yaml")
    def test_list_sms_numbers_basic(self, email_client, basic_sms_numbers_list_request):
        """Test listing SMS numbers with basic parameters."""
        response = email_client.sms_numbers.list(basic_sms_numbers_list_request)

        assert isinstance(response, APIResponse)
        assert response.status_code == 200
        assert response.data is not None

        # Check that we have the expected structure
        if "data" in response.data:
            sms_numbers = response.data["data"]
            assert isinstance(sms_numbers, list)

            # If we have SMS numbers, check the structure
            if sms_numbers:
                first_sms_number = sms_numbers[0]
                assert "id" in first_sms_number
                assert "telephone_number" in first_sms_number
                assert "paused" in first_sms_number
                assert "created_at" in first_sms_number

    @vcr.use_cassette("sms_numbers_list_with_filters.yaml")
    def test_list_sms_numbers_with_filters(self, email_client, sms_numbers_list_request_with_filters):
        """Test listing SMS numbers with filters."""
        response = email_client.sms_numbers.list(sms_numbers_list_request_with_filters)

        assert isinstance(response, APIResponse)
        assert response.status_code == 200

        # Check pagination metadata
        if "meta" in response.data:
            meta = response.data["meta"]
            assert "current_page" in meta or "page" in meta
            assert "per_page" in meta or "limit" in meta

    @vcr.use_cassette("sms_numbers_list_paused_only.yaml")
    def test_list_sms_numbers_paused_only(self, email_client):
        """Test listing only paused SMS numbers."""
        request = SmsNumbersListRequest(paused=True, limit=10)

        response = email_client.sms_numbers.list(request)

        assert isinstance(response, APIResponse)
        assert response.status_code == 200

        # Check that if we have SMS numbers, they are all paused
        if "data" in response.data and response.data["data"]:
            for sms_number in response.data["data"]:
                assert sms_number.get("paused") is True

    @vcr.use_cassette("sms_numbers_list_active_only.yaml")
    def test_list_sms_numbers_active_only(self, email_client):
        """Test listing only active (non-paused) SMS numbers."""
        request = SmsNumbersListRequest(paused=False, limit=10)

        response = email_client.sms_numbers.list(request)

        assert isinstance(response, APIResponse)
        assert response.status_code == 200

        # Check that if we have SMS numbers, they are all active
        if "data" in response.data and response.data["data"]:
            for sms_number in response.data["data"]:
                assert sms_number.get("paused") is False

    # ============================================================================
    # SMS Number Get Tests
    # ============================================================================

    @vcr.use_cassette("sms_numbers_get_not_found.yaml")
    def test_get_sms_number_not_found_with_test_id(self, email_client, sms_number_get_request):
        """Test getting a non-existent SMS number returns 404."""
        from mailersend.exceptions import ResourceNotFoundError
        
        with pytest.raises(ResourceNotFoundError) as exc_info:
            email_client.sms_numbers.get(sms_number_get_request)

        error_str = str(exc_info.value).lower()
        assert ("not found" in error_str or "404" in error_str or 
                "could not be found" in error_str or 
                "sms" in error_str or "number" in error_str)

    # ============================================================================
    # SMS Number Update Tests
    # ============================================================================

    @vcr.use_cassette("sms_numbers_update_not_found.yaml")
    def test_update_sms_number_not_found_with_test_id(self, email_client, sms_number_update_request):
        """Test updating a non-existent SMS number returns 404."""
        from mailersend.exceptions import ResourceNotFoundError
        
        with pytest.raises(ResourceNotFoundError) as exc_info:
            email_client.sms_numbers.update(sms_number_update_request)

        error_str = str(exc_info.value).lower()
        assert ("not found" in error_str or "404" in error_str or 
                "could not be found" in error_str or 
                "sms" in error_str or "number" in error_str)

    @vcr.use_cassette("sms_numbers_update_pause.yaml")
    def test_update_sms_number_pause(self, email_client, sms_number_id_from_env):
        """Test pausing an SMS number."""
        from mailersend.exceptions import ResourceNotFoundError
        
        request = SmsNumberUpdateRequest(
            sms_number_id=sms_number_id_from_env,
            paused=True
        )

        # This will likely fail with 404 for test SMS number ID
        with pytest.raises(ResourceNotFoundError) as exc_info:
            email_client.sms_numbers.update(request)

        error_str = str(exc_info.value).lower()
        assert ("not found" in error_str or "404" in error_str or 
                "could not be found" in error_str or 
                "sms" in error_str or "number" in error_str)

    @vcr.use_cassette("sms_numbers_update_unpause.yaml")
    def test_update_sms_number_unpause(self, email_client, sms_number_id_from_env):
        """Test unpausing an SMS number."""
        from mailersend.exceptions import ResourceNotFoundError
        
        request = SmsNumberUpdateRequest(
            sms_number_id=sms_number_id_from_env,
            paused=False
        )

        # This will likely fail with 404 for test SMS number ID
        with pytest.raises(ResourceNotFoundError) as exc_info:
            email_client.sms_numbers.update(request)

        error_str = str(exc_info.value).lower()
        assert ("not found" in error_str or "404" in error_str or 
                "could not be found" in error_str or 
                "sms" in error_str or "number" in error_str)

    # ============================================================================
    # SMS Number Delete Tests
    # ============================================================================

    @vcr.use_cassette("sms_numbers_delete_not_found.yaml")
    def test_delete_sms_number_not_found_with_test_id(self, email_client, sms_number_delete_request):
        """Test deleting a non-existent SMS number returns 404."""
        from mailersend.exceptions import ResourceNotFoundError
        
        with pytest.raises(ResourceNotFoundError) as exc_info:
            email_client.sms_numbers.delete(sms_number_delete_request)

        error_str = str(exc_info.value).lower()
        assert ("not found" in error_str or "404" in error_str or 
                "could not be found" in error_str or 
                "sms" in error_str or "number" in error_str)

    # ============================================================================
    # Validation and Error Handling Tests
    # ============================================================================

    @vcr.use_cassette("sms_numbers_validation_error.yaml")
    def test_list_sms_numbers_validation_error(self, email_client):
        """Test that invalid request raises validation error."""
        with pytest.raises(Exception) as exc_info:
            # Pass invalid request type
            email_client.sms_numbers.list("invalid-request")

        # Should raise an AttributeError for invalid request type
        error_str = str(exc_info.value).lower()
        assert (
            "attribute" in error_str
            or "to_query_params" in error_str
        )

    @vcr.use_cassette("sms_numbers_api_response_structure.yaml")
    def test_api_response_structure(self, email_client, basic_sms_numbers_list_request):
        """Test that API response has the expected structure and metadata."""
        response = email_client.sms_numbers.list(basic_sms_numbers_list_request)

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

    @vcr.use_cassette("sms_numbers_empty_result.yaml")
    def test_list_sms_numbers_empty_result(self, email_client, basic_sms_numbers_list_request):
        """Test listing SMS numbers when no SMS numbers exist."""
        response = email_client.sms_numbers.list(basic_sms_numbers_list_request)

        assert isinstance(response, APIResponse)
        assert response.status_code == 200
        assert response.data is not None

        # Should have data array (may not be empty due to existing SMS numbers)
        if "data" in response.data:
            assert isinstance(response.data["data"], list)

    # ============================================================================
    # Model Validation Tests
    # ============================================================================

    def test_sms_number_get_model_validation(self):
        """Test model validation for SMS number get request."""
        # Test empty SMS number ID
        with pytest.raises(ValueError):
            SmsNumberGetRequest(sms_number_id="")

        # Test valid SMS number ID
        request = SmsNumberGetRequest(sms_number_id="valid-sms-number-id")
        assert request.sms_number_id == "valid-sms-number-id"

    def test_sms_number_update_model_validation(self):
        """Test model validation for SMS number update request."""
        # Test empty SMS number ID
        with pytest.raises(ValueError):
            SmsNumberUpdateRequest(sms_number_id="")

        # Test valid update request with paused=True
        request = SmsNumberUpdateRequest(
            sms_number_id="valid-sms-number-id",
            paused=True
        )
        assert request.sms_number_id == "valid-sms-number-id"
        assert request.paused is True

        # Test valid update request with paused=False
        request2 = SmsNumberUpdateRequest(
            sms_number_id="valid-sms-number-id",
            paused=False
        )
        assert request2.paused is False

        # Test update request without paused field (should be None)
        request3 = SmsNumberUpdateRequest(sms_number_id="valid-sms-number-id")
        assert request3.paused is None

    def test_sms_number_delete_model_validation(self):
        """Test model validation for SMS number delete request."""
        # Test empty SMS number ID
        with pytest.raises(ValueError):
            SmsNumberDeleteRequest(sms_number_id="")

        # Test valid SMS number ID
        request = SmsNumberDeleteRequest(sms_number_id="valid-sms-number-id")
        assert request.sms_number_id == "valid-sms-number-id"

    def test_sms_numbers_list_query_params(self):
        """Test SMS numbers list query parameters."""
        # Test basic request (no filters)
        request = SmsNumbersListRequest()
        params = request.to_query_params()
        assert params == {}

        # Test with paused filter
        request_paused = SmsNumbersListRequest(paused=True)
        params_paused = request_paused.to_query_params()
        assert params_paused["paused"] == "true"

        # Test with all filters
        request_all = SmsNumbersListRequest(
            paused=False,
            page=2,
            limit=25
        )
        params_all = request_all.to_query_params()
        assert params_all["paused"] == "false"
        assert params_all["page"] == 2
        assert params_all["limit"] == 25

    def test_sms_number_update_to_json(self):
        """Test SMS number update request JSON conversion."""
        # Test with paused=True
        request = SmsNumberUpdateRequest(
            sms_number_id="test-id",
            paused=True
        )
        
        json_data = request.to_json()
        assert json_data["paused"] is True
        assert "sms_number_id" not in json_data  # ID goes in URL, not body

        # Test with paused=False
        request2 = SmsNumberUpdateRequest(
            sms_number_id="test-id",
            paused=False
        )
        
        json_data2 = request2.to_json()
        assert json_data2["paused"] is False

        # Test without paused field
        request3 = SmsNumberUpdateRequest(sms_number_id="test-id")
        
        json_data3 = request3.to_json()
        assert json_data3 == {}  # Empty payload when no fields to update

    def test_sms_numbers_list_boolean_conversion(self):
        """Test boolean conversion in query parameters."""
        # Test True converts to lowercase "true"
        request_true = SmsNumbersListRequest(paused=True)
        params_true = request_true.to_query_params()
        assert params_true["paused"] == "true"

        # Test False converts to lowercase "false"
        request_false = SmsNumbersListRequest(paused=False)
        params_false = request_false.to_query_params()
        assert params_false["paused"] == "false"

        # Test None is not included in params
        request_none = SmsNumbersListRequest(paused=None)
        params_none = request_none.to_query_params()
        assert "paused" not in params_none

    def test_sms_number_id_validation_edge_cases(self):
        """Test SMS number ID validation edge cases."""
        # Test empty string ID should fail (min_length=1)
        with pytest.raises(ValueError):
            SmsNumberGetRequest(sms_number_id="")

        # Test whitespace-only ID is allowed by pydantic min_length validation
        # (min_length counts characters, not meaningful content)
        request_whitespace = SmsNumberGetRequest(sms_number_id="   ")
        assert request_whitespace.sms_number_id == "   "

        # Test very long but valid ID
        long_id = "a" * 100
        request = SmsNumberGetRequest(sms_number_id=long_id)
        assert request.sms_number_id == long_id

        # Test ID with special characters
        special_id = "sms-number-123-abc_def"
        request2 = SmsNumberGetRequest(sms_number_id=special_id)
        assert request2.sms_number_id == special_id

    def test_sms_numbers_list_parameter_combinations(self):
        """Test various parameter combinations for SMS numbers list."""
        # Test only page parameter
        request_page = SmsNumbersListRequest(page=5)
        params_page = request_page.to_query_params()
        assert params_page == {"page": 5}

        # Test only limit parameter
        request_limit = SmsNumbersListRequest(limit=50)
        params_limit = request_limit.to_query_params()
        assert params_limit == {"limit": 50}

        # Test page and limit together
        request_both = SmsNumbersListRequest(page=3, limit=20)
        params_both = request_both.to_query_params()
        assert params_both == {"page": 3, "limit": 20}

        # Test all parameters with None values
        request_all_none = SmsNumbersListRequest(
            paused=None,
            page=None,
            limit=None
        )
        params_all_none = request_all_none.to_query_params()
        assert params_all_none == {} 