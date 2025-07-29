import pytest
from unittest.mock import Mock, patch
from requests import Response

from mailersend.resources.activity import Activity
from mailersend.models.activity import ActivityRequest, ActivityQueryParams, SingleActivityRequest
from mailersend.models.base import APIResponse
from mailersend.exceptions import ValidationError


class TestActivityResource:
    """Test the Activity resource class."""

    @pytest.fixture
    def activity_resource(self):
        """Create an Activity resource instance with a mocked client."""
        mock_client = Mock()
        return Activity(mock_client)

    @pytest.fixture
    def mock_response(self):
        """Create a mock HTTP response."""
        response = Mock(spec=Response)
        response.status_code = 200
        response.headers = {"Content-Type": "application/json"}
        response.json.return_value = {
            "data": {
                "id": "5ee0b166b251345e407c9207",
                "created_at": "2020-06-04 12:00:00",
                "updated_at": "2020-06-04 12:00:00",
                "type": "clicked",
                "email": {
                    "id": "5ee0b166b251345e407c9201",
                    "from": "colleen.wiza@example.net",
                    "subject": "Magni aperiam sunt nam omnis.",
                    "text": "Lorem ipsum dolor sit amet, consectetuer adipiscin",
                    "html": "<html><body><a href='https://www.mailersend.com' t",
                    "status": "sent",
                    "tags": None,
                    "created_at": "2020-06-04 12:00:00",
                    "updated_at": "2020-06-04 12:00:00",
                    "recipient": {
                        "id": "5ee0b166b251345e407c9200",
                        "email": "tyra.cummerata@example.org",
                        "created_at": "2020-06-04 12:00:00",
                        "updated_at": "2020-06-04 12:00:00",
                        "deleted_at": ""
                    }
                }
            }
        }
        return response

    def test_get_single_success(self, activity_resource, mock_response):
        """Test successful retrieval of a single activity."""
        activity_id = "5ee0b166b251345e407c9207"
        request = SingleActivityRequest(activity_id=activity_id)
        
        # Mock the client request
        activity_resource.client.request.return_value = mock_response
        
        # Call the method
        result = activity_resource.get_single(request)
        
        # Verify the client was called correctly
        activity_resource.client.request.assert_called_once_with(
            method="GET", endpoint=f"activities/{activity_id}"
        )
        
        # Verify the result
        assert isinstance(result, APIResponse)
        assert result.status_code == 200
        assert result["data"]["id"] == activity_id
        assert result["data"]["type"] == "clicked"

    def test_get_single_with_whitespace(self, activity_resource, mock_response):
        """Test that whitespace is stripped from activity_id."""
        activity_id = "  5ee0b166b251345e407c9207  "
        expected_id = "5ee0b166b251345e407c9207"
        request = SingleActivityRequest(activity_id=activity_id)
        
        activity_resource.client.request.return_value = mock_response
        
        result = activity_resource.get_single(request)
        
        # Verify the client was called with stripped ID
        activity_resource.client.request.assert_called_once_with(
            method="GET", endpoint=f"activities/{expected_id}"
        )
        
        assert isinstance(result, APIResponse)

    def test_get_single_empty_activity_id(self, activity_resource):
        """Test that empty activity_id raises ValidationError."""
        with pytest.raises(ValueError) as exc_info:
            SingleActivityRequest(activity_id="")
        
        assert "activity_id cannot be empty" in str(exc_info.value)
        activity_resource.client.request.assert_not_called()

    def test_get_single_whitespace_only_activity_id(self, activity_resource):
        """Test that whitespace-only activity_id raises ValidationError."""
        with pytest.raises(ValueError) as exc_info:
            SingleActivityRequest(activity_id="   ")
        
        assert "activity_id cannot be empty" in str(exc_info.value)
        activity_resource.client.request.assert_not_called()

    def test_get_single_none_request(self, activity_resource):
        """Test that None request raises AttributeError."""
        with pytest.raises(AttributeError):
            activity_resource.get_single(None)

    def test_get_single_invalid_request_type(self, activity_resource):
        """Test that invalid request type raises AttributeError."""
        with pytest.raises(AttributeError):
            activity_resource.get_single("invalid_request")

    def test_get_single_logging(self, activity_resource, mock_response):
        """Test that appropriate logging occurs."""
        activity_id = "5ee0b166b251345e407c9207"
        request = SingleActivityRequest(activity_id=activity_id)
        activity_resource.client.request.return_value = mock_response
        
        with patch.object(activity_resource, 'logger') as mock_logger:
            result = activity_resource.get_single(request)
            
            # Verify debug logging was called
            mock_logger.debug.assert_called()

    def test_get_single_error_logging(self, activity_resource):
        """Test that error occurs for invalid input."""
        with pytest.raises(AttributeError):
            activity_resource.get_single(None)

    def test_get_single_api_response_structure(self, activity_resource, mock_response):
        """Test that the API response structure is properly handled."""
        activity_id = "5ee0b166b251345e407c9207"
        request = SingleActivityRequest(activity_id=activity_id)
        activity_resource.client.request.return_value = mock_response
        
        result = activity_resource.get_single(request)
        
        # Verify response structure
        assert "data" in result
        data = result["data"]
        assert "id" in data
        assert "type" in data
        assert "email" in data
        assert "created_at" in data
        assert "updated_at" in data
        
        # Verify email structure
        email = data["email"]
        assert "id" in email
        assert "from" in email
        assert "subject" in email
        assert "recipient" in email
        
        # Verify recipient structure
        recipient = email["recipient"]
        assert "id" in recipient
        assert "email" in recipient 