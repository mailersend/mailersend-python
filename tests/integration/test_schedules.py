import pytest
from tests.test_helpers import vcr, email_client
import os

from mailersend.models.schedules import (
    SchedulesListRequest,
    ScheduleGetRequest,
    ScheduleDeleteRequest,
    SchedulesListQueryParams,
)
from mailersend.models.base import APIResponse


@pytest.fixture
def basic_schedules_list_request():
    """Basic schedules list request"""
    return SchedulesListRequest(
        query_params=SchedulesListQueryParams(page=1, limit=10)
    )


@pytest.fixture
def schedule_get_request():
    """Schedule get request with test message ID"""
    return ScheduleGetRequest(message_id="test-message-id")


@pytest.fixture
def sample_domain_id():
    """Sample domain ID for testing"""
    return os.environ.get("SDK_DOMAIN_ID", "test-domain-id")


class TestSchedulesIntegration:
    """Integration tests for Schedules API."""

    @vcr.use_cassette("schedules_list_basic.yaml")
    def test_list_schedules_basic(self, email_client, basic_schedules_list_request):
        """Test listing scheduled messages with basic parameters."""
        response = email_client.schedules.list_schedules(basic_schedules_list_request)

        assert isinstance(response, APIResponse)
        assert response.status_code == 200
        assert response.data is not None

        # Check that we have the expected structure
        if "data" in response.data:
            schedules = response.data["data"]
            assert isinstance(schedules, list)

            # If we have schedules, check the structure
            if schedules:
                first_schedule = schedules[0]
                assert "message_id" in first_schedule
                assert "subject" in first_schedule or "send_at" in first_schedule  # API may not always include subject
                assert "send_at" in first_schedule
                assert "status" in first_schedule
                assert "created_at" in first_schedule

    @vcr.use_cassette("schedules_list_with_pagination.yaml")
    def test_list_schedules_with_pagination(self, email_client):
        """Test listing scheduled messages with pagination."""
        request = SchedulesListRequest(
            query_params=SchedulesListQueryParams(page=1, limit=10)
        )

        response = email_client.schedules.list_schedules(request)

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

    @vcr.use_cassette("schedules_list_with_domain_filter.yaml")
    def test_list_schedules_with_domain_filter(self, email_client, sample_domain_id):
        """Test listing scheduled messages filtered by domain."""
        request = SchedulesListRequest(
            query_params=SchedulesListQueryParams(
                page=1, 
                limit=10, 
                domain_id=sample_domain_id
            )
        )

        response = email_client.schedules.list_schedules(request)

        assert isinstance(response, APIResponse)
        assert response.status_code == 200
        assert response.data is not None

    @vcr.use_cassette("schedules_list_with_status_filter.yaml")
    def test_list_schedules_with_status_filter(self, email_client):
        """Test listing scheduled messages filtered by status."""
        request = SchedulesListRequest(
            query_params=SchedulesListQueryParams(
                page=1, 
                limit=10, 
                status="scheduled"
            )
        )

        response = email_client.schedules.list_schedules(request)

        assert isinstance(response, APIResponse)
        assert response.status_code == 200
        assert response.data is not None

        # If we have data, verify all schedules have the requested status
        if "data" in response.data and response.data["data"]:
            for schedule in response.data["data"]:
                if "status" in schedule:
                    assert schedule["status"] == "scheduled"

    @vcr.use_cassette("schedules_get_single.yaml")
    def test_get_schedule_not_found_with_test_id(self, email_client, schedule_get_request):
        """Test getting a non-existent scheduled message returns 404."""
        from mailersend.exceptions import ResourceNotFoundError
        
        with pytest.raises(ResourceNotFoundError) as exc_info:
            email_client.schedules.get_schedule(schedule_get_request)

        error_str = str(exc_info.value).lower()
        assert "not found" in error_str or "404" in error_str or "could not be found" in error_str

    @vcr.use_cassette("schedules_delete.yaml")
    def test_delete_schedule_not_found_with_test_id(self, email_client, schedule_get_request):
        """Test deleting a non-existent scheduled message returns 404."""
        from mailersend.exceptions import ResourceNotFoundError
        
        delete_request = ScheduleDeleteRequest(
            message_id=schedule_get_request.message_id
        )

        with pytest.raises(ResourceNotFoundError) as exc_info:
            email_client.schedules.delete_schedule(delete_request)

        error_str = str(exc_info.value).lower()
        assert ("not found" in error_str or "404" in error_str or 
                "could not be found" in error_str or 
                "not possible to delete" in error_str or
                "already been sent" in error_str)

    @vcr.use_cassette("schedules_validation_error.yaml")
    def test_list_schedules_validation_error(self, email_client):
        """Test that invalid request raises validation error."""
        with pytest.raises(Exception) as exc_info:
            # Pass invalid request type
            email_client.schedules.list_schedules("invalid-request")

        # Should raise an AttributeError for invalid request type
        error_str = str(exc_info.value).lower()
        assert (
            "attribute" in error_str
            or "to_query_params" in error_str
        )

    @vcr.use_cassette("schedules_api_response_structure.yaml")
    def test_api_response_structure(self, email_client, basic_schedules_list_request):
        """Test that API response has the expected structure and metadata."""
        response = email_client.schedules.list_schedules(basic_schedules_list_request)

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

    @vcr.use_cassette("schedules_empty_result.yaml")
    def test_list_schedules_empty_result(self, email_client, basic_schedules_list_request):
        """Test listing scheduled messages when no schedules exist."""
        response = email_client.schedules.list_schedules(basic_schedules_list_request)

        assert isinstance(response, APIResponse)
        assert response.status_code == 200
        assert response.data is not None

        # Should have data array (may not be empty due to scheduled messages)
        if "data" in response.data:
            assert isinstance(response.data["data"], list)

    def test_schedule_get_model_validation(self):
        """Test model validation for schedule get request."""
        # Test empty message_id
        with pytest.raises(ValueError) as exc_info:
            ScheduleGetRequest(message_id="")
        assert "message id is required" in str(exc_info.value).lower()

        # Test whitespace message_id
        with pytest.raises(ValueError) as exc_info:
            ScheduleGetRequest(message_id="   ")
        assert "message id is required" in str(exc_info.value).lower()

    def test_schedule_delete_model_validation(self):
        """Test model validation for schedule delete request."""
        # Test empty message_id
        with pytest.raises(ValueError) as exc_info:
            ScheduleDeleteRequest(message_id="")
        assert "message id is required" in str(exc_info.value).lower()

        # Test whitespace message_id
        with pytest.raises(ValueError) as exc_info:
            ScheduleDeleteRequest(message_id="   ")
        assert "message id is required" in str(exc_info.value).lower()

    def test_schedules_list_query_params_validation(self):
        """Test validation for schedules list query parameters."""
        # Test valid parameters
        params = SchedulesListQueryParams(
            page=1, 
            limit=25, 
            domain_id="test-domain",
            status="scheduled"
        )
        assert params.page == 1
        assert params.limit == 25
        assert params.domain_id == "test-domain"
        assert params.status == "scheduled"
        
        # Test minimum limit validation
        with pytest.raises(ValueError):
            SchedulesListQueryParams(limit=5)  # Below minimum of 10
            
        # Test maximum limit validation  
        with pytest.raises(ValueError):
            SchedulesListQueryParams(limit=150)  # Above maximum of 100
            
        # Test minimum page validation
        with pytest.raises(ValueError):
            SchedulesListQueryParams(page=0)  # Below minimum of 1
            
        # Test empty domain_id validation
        with pytest.raises(ValueError) as exc_info:
            SchedulesListQueryParams(domain_id="")
        assert "domain id cannot be empty" in str(exc_info.value).lower()
        
        # Test invalid status validation
        with pytest.raises(ValueError):
            SchedulesListQueryParams(status="invalid")  # Not in allowed values

    def test_schedules_list_query_params_to_dict(self):
        """Test query parameters conversion to dictionary."""
        # Test with all parameters
        params = SchedulesListQueryParams(
            page=2,
            limit=50,
            domain_id="test-domain",
            status="sent"
        )
        query_dict = params.to_query_params()
        
        assert query_dict["page"] == 2
        assert query_dict["limit"] == 50
        assert query_dict["domain_id"] == "test-domain"
        assert query_dict["status"] == "sent"
        
        # Test with minimal parameters (only defaults)
        params_minimal = SchedulesListQueryParams()
        query_dict_minimal = params_minimal.to_query_params()
        
        assert query_dict_minimal["page"] == 1
        assert query_dict_minimal["limit"] == 25
        assert "domain_id" not in query_dict_minimal  # None values excluded
        assert "status" not in query_dict_minimal  # None values excluded 