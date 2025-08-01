"""Unit tests for Schedules resource."""
import pytest
from unittest.mock import Mock, MagicMock

from mailersend.resources.schedules import Schedules
from mailersend.models.base import APIResponse
from mailersend.models.schedules import (
    SchedulesListRequest,
    SchedulesListQueryParams,
    ScheduleGetRequest,
    ScheduleDeleteRequest,
)
from mailersend.exceptions import ValidationError as MailerSendValidationError


class TestSchedules:
    """Test Schedules resource class."""

    def setup_method(self):
        """Set up test fixtures."""
        self.mock_client = Mock()
        self.resource = Schedules(self.mock_client)
        self.resource.logger = Mock()

        # Mock _create_response method
        self.mock_api_response = MagicMock(spec=APIResponse)
        self.resource._create_response = Mock(return_value=self.mock_api_response)

    def test_list_schedules_returns_api_response(self):
        """Test list_schedules method returns APIResponse."""
        query_params = SchedulesListQueryParams()
        request = SchedulesListRequest(query_params=query_params)

        mock_response = Mock()
        self.mock_client.request.return_value = mock_response

        result = self.resource.list_schedules(request)

        assert result == self.mock_api_response
        self.resource._create_response.assert_called_once_with(mock_response)

    def test_list_schedules_uses_query_params(self):
        """Test list_schedules method uses query params correctly."""
        query_params = SchedulesListQueryParams(
            domain_id="test-domain", status="scheduled", page=2, limit=50
        )
        request = SchedulesListRequest(query_params=query_params)

        mock_response = Mock()
        self.mock_client.request.return_value = mock_response

        result = self.resource.list_schedules(request)

        # Verify client was called correctly
        self.mock_client.request.assert_called_once_with(
            method="GET",
            path="message-schedules",
            params={
                "domain_id": "test-domain",
                "status": "scheduled",
                "page": 2,
                "limit": 50,
            },
        )

        # Verify _create_response was called
        self.resource._create_response.assert_called_once_with(mock_response)

    def test_list_schedules_with_defaults(self):
        """Test list_schedules with default query params."""
        query_params = SchedulesListQueryParams()
        request = SchedulesListRequest(query_params=query_params)

        mock_response = Mock()
        self.mock_client.request.return_value = mock_response

        result = self.resource.list_schedules(request)

        # Verify client was called with defaults
        self.mock_client.request.assert_called_once_with(
            method="GET", path="message-schedules", params={"page": 1, "limit": 25}
        )

    def test_list_schedules_excludes_none_values(self):
        """Test list_schedules excludes None values from params."""
        query_params = SchedulesListQueryParams(page=1, limit=25)
        request = SchedulesListRequest(query_params=query_params)

        mock_response = Mock()
        self.mock_client.request.return_value = mock_response

        result = self.resource.list_schedules(request)

        # Verify None values are excluded from params
        call_args = self.mock_client.request.call_args
        params = call_args[1]["params"]
        assert "domain_id" not in params
        assert "status" not in params
        for key, value in params.items():
            assert value is not None

    def test_get_schedule_returns_api_response(self):
        """Test get_schedule method returns APIResponse."""
        request = ScheduleGetRequest(message_id="message123")

        mock_response = Mock()
        self.mock_client.request.return_value = mock_response

        result = self.resource.get_schedule(request)

        assert result == self.mock_api_response
        self.resource._create_response.assert_called_once_with(mock_response)

    def test_get_schedule_with_valid_request(self):
        """Test get_schedule with valid request."""
        request = ScheduleGetRequest(message_id="message123")

        mock_response = Mock()
        self.mock_client.request.return_value = mock_response

        result = self.resource.get_schedule(request)

        # Verify client was called correctly
        self.mock_client.request.assert_called_once_with(
            method="GET", path="message-schedules/message123"
        )

    def test_get_schedule_endpoint_construction(self):
        """Test get_schedule constructs endpoint correctly."""
        request = ScheduleGetRequest(message_id="61e01f471053b349a5478a52")

        mock_response = Mock()
        self.mock_client.request.return_value = mock_response

        result = self.resource.get_schedule(request)

        # Verify endpoint construction
        self.mock_client.request.assert_called_once_with(
            method="GET", path="message-schedules/61e01f471053b349a5478a52"
        )

    def test_delete_schedule_returns_api_response(self):
        """Test delete_schedule method returns APIResponse."""
        request = ScheduleDeleteRequest(message_id="message123")

        mock_response = Mock()
        self.mock_client.request.return_value = mock_response

        result = self.resource.delete_schedule(request)

        assert result == self.mock_api_response
        self.resource._create_response.assert_called_once_with(mock_response)

    def test_delete_schedule_with_valid_request(self):
        """Test delete_schedule with valid request."""
        request = ScheduleDeleteRequest(message_id="message123")

        mock_response = Mock()
        self.mock_client.request.return_value = mock_response

        result = self.resource.delete_schedule(request)

        # Verify client was called correctly
        self.mock_client.request.assert_called_once_with(
            method="DELETE", path="message-schedules/message123"
        )

    def test_delete_schedule_endpoint_construction(self):
        """Test delete_schedule constructs endpoint correctly."""
        request = ScheduleDeleteRequest(message_id="61e01f471053b349a5478a52")

        mock_response = Mock()
        self.mock_client.request.return_value = mock_response

        result = self.resource.delete_schedule(request)

        # Verify endpoint construction
        self.mock_client.request.assert_called_once_with(
            method="DELETE", path="message-schedules/61e01f471053b349a5478a52"
        )

    def test_integration_workflow(self):
        """Test integration workflow with multiple operations."""
        # Setup different requests for different methods
        query_params = SchedulesListQueryParams()
        request_list = SchedulesListRequest(query_params=query_params)
        request_get = ScheduleGetRequest(message_id="message123")
        request_delete = ScheduleDeleteRequest(message_id="message123")

        # Test that each method returns the expected APIResponse type
        assert isinstance(
            self.resource.list_schedules(request_list), type(self.mock_api_response)
        )
        assert isinstance(
            self.resource.get_schedule(request_get), type(self.mock_api_response)
        )
        assert isinstance(
            self.resource.delete_schedule(request_delete), type(self.mock_api_response)
        )
