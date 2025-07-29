import pytest
from unittest.mock import Mock
import requests

from mailersend.resources.analytics import Analytics
from mailersend.models.analytics import AnalyticsRequest
from mailersend.models.base import APIResponse
from mailersend.exceptions import ValidationError


class TestAnalyticsResource:
    """Test Analytics resource functionality"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.mock_client = Mock()
        self.mock_logger = Mock()
        self.analytics = Analytics(self.mock_client, self.mock_logger)
        
        # Create a sample analytics request
        self.sample_request = AnalyticsRequest(
            date_from=1443651141,
            date_to=1443661141,
            tags=["newsletter", "marketing"],
            event=["sent", "delivered", "opened"]
        )
    
    def test_get_activity_by_date_success(self):
        """Test successful activity by date request"""
        # Mock response
        mock_response = Mock(spec=requests.Response)
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": {
                "date_from": "1443651141",
                "date_to": "1443661141",
                "group_by": "days",
                "stats": [
                    {
                        "date": "1443651141",
                        "sent": 100,
                        "delivered": 95,
                        "opened": 30
                    }
                ]
            }
        }
        mock_response.headers = Mock()
        mock_response.headers.get.return_value = "test-request-id"
        mock_response.headers.__iter__ = Mock(return_value=iter(["x-request-id"]))
        mock_response.headers.keys = Mock(return_value=["x-request-id"])
        mock_response.headers.__getitem__ = Mock(return_value="test-request-id")
        mock_response.content = b'{"data": {"stats": []}}'
        
        self.mock_client.request.return_value = mock_response
        
        # Make request
        result = self.analytics.get_activity_by_date(self.sample_request)
        
        # Assertions
        assert isinstance(result, APIResponse)
        self.mock_client.request.assert_called_once()
        call_args = self.mock_client.request.call_args
        assert call_args[0] == ("GET", "analytics/date")
        assert "params" in call_args[1]
        
        # Check that the right parameters were passed
        params = call_args[1]["params"]
        assert "date_from" in params
        assert "date_to" in params
        assert "tags[]" in params
        assert "event[]" in params
    
    def test_get_activity_by_date_no_request(self):
        """Test activity by date with no request object"""
        with pytest.raises(AttributeError):
            self.analytics.get_activity_by_date(None)
    
    def test_get_activity_by_date_no_events(self):
        """Test activity by date with no events specified"""
        request_without_events = AnalyticsRequest(
            date_from=1443651141,
            date_to=1443661141
        )
        
        # Mock response
        mock_response = Mock(spec=requests.Response)
        mock_response.status_code = 200
        mock_response.headers = Mock()
        mock_response.headers.get.return_value = "test-request-id"
        mock_response.headers.__iter__ = Mock(return_value=iter(["x-request-id"]))
        mock_response.headers.keys = Mock(return_value=["x-request-id"])
        mock_response.headers.__getitem__ = Mock(return_value="test-request-id")
        mock_response.content = b'{"data": {"stats": []}}'
        mock_response.json.return_value = {"data": {"stats": []}}
        
        self.mock_client.request.return_value = mock_response
        
        # This should work fine - no events is valid for the request model
        result = self.analytics.get_activity_by_date(request_without_events)
        assert isinstance(result, APIResponse)
    
    def test_get_opens_by_country_success(self):
        """Test successful opens by country request"""
        # Mock response
        mock_response = Mock(spec=requests.Response)
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": {
                "date_from": 1443651141,
                "date_to": 1443661141,
                "stats": [
                    {"name": "LT", "count": 25},
                    {"name": "US", "count": 50}
                ]
            }
        }
        mock_response.headers = Mock()
        mock_response.headers.get.return_value = "test-request-id"
        mock_response.headers.__iter__ = Mock(return_value=iter(["x-request-id"]))
        mock_response.headers.keys = Mock(return_value=["x-request-id"])
        mock_response.headers.__getitem__ = Mock(return_value="test-request-id")
        mock_response.content = b'{"data": {"stats": []}}'
        
        self.mock_client.request.return_value = mock_response
        
        # Make request
        result = self.analytics.get_opens_by_country(self.sample_request)
        
        # Assertions
        assert isinstance(result, APIResponse)
        self.mock_client.request.assert_called_once()
        call_args = self.mock_client.request.call_args
        assert call_args[0] == ("GET", "analytics/country")
        
        # Check that excluded fields are not present
        params = call_args[1]["params"]
        assert "event" not in params
        assert "group_by" not in params
        assert "date_from" in params
        assert "date_to" in params
    
    def test_get_opens_by_user_agent_success(self):
        """Test successful opens by user agent request"""
        # Mock response
        mock_response = Mock(spec=requests.Response)
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": {
                "date_from": 1443651141,
                "date_to": 1443661141,
                "stats": [
                    {"name": "Chrome", "count": 75},
                    {"name": "Firefox", "count": 20}
                ]
            }
        }
        mock_response.headers = Mock()
        mock_response.headers.get.return_value = "test-request-id"
        mock_response.headers.__iter__ = Mock(return_value=iter(["x-request-id"]))
        mock_response.headers.keys = Mock(return_value=["x-request-id"])
        mock_response.headers.__getitem__ = Mock(return_value="test-request-id")
        mock_response.content = b'{"data": {"stats": []}}'
        
        self.mock_client.request.return_value = mock_response
        
        # Make request
        result = self.analytics.get_opens_by_user_agent(self.sample_request)
        
        # Assertions
        assert isinstance(result, APIResponse)
        self.mock_client.request.assert_called_once()
        call_args = self.mock_client.request.call_args
        assert call_args[0] == ("GET", "analytics/ua-name")
    
    def test_get_opens_by_reading_environment_success(self):
        """Test successful opens by reading environment request"""
        # Mock response
        mock_response = Mock(spec=requests.Response)
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": {
                "date_from": 1443651141,
                "date_to": 1443661141,
                "stats": [
                    {"name": "webmail", "count": 45},
                    {"name": "mobile", "count": 30},
                    {"name": "desktop", "count": 25}
                ]
            }
        }
        mock_response.headers = Mock()
        mock_response.headers.get.return_value = "test-request-id"
        mock_response.headers.__iter__ = Mock(return_value=iter(["x-request-id"]))
        mock_response.headers.keys = Mock(return_value=["x-request-id"])
        mock_response.headers.__getitem__ = Mock(return_value="test-request-id")
        mock_response.content = b'{"data": {"stats": []}}'
        
        self.mock_client.request.return_value = mock_response
        
        # Make request
        result = self.analytics.get_opens_by_reading_environment(self.sample_request)
        
        # Assertions
        assert isinstance(result, APIResponse)
        self.mock_client.request.assert_called_once()
        call_args = self.mock_client.request.call_args
        assert call_args[0] == ("GET", "analytics/ua-type")
    
    def test_build_query_params_basic(self):
        """Test basic query parameter building"""
        request = AnalyticsRequest(
            date_from=1443651141,
            date_to=1443661141,
            tags=["newsletter"],
            event=["sent", "delivered"]
        )
        
        params = self.analytics._build_query_params(request)
        
        assert params["date_from"] == 1443651141
        assert params["date_to"] == 1443661141
        assert params["tags[]"] == ["newsletter"]
        assert params["event[]"] == ["sent", "delivered"]
        assert params["group_by"] == "days"
    
    def test_build_query_params_with_exclusions(self):
        """Test query parameter building with field exclusions"""
        request = AnalyticsRequest(
            date_from=1443651141,
            date_to=1443661141,
            tags=["newsletter"],
            event=["sent", "delivered"],
            group_by="weeks"
        )
        
        params = self.analytics._build_query_params(request, exclude_fields=["event", "group_by"])
        
        assert params["date_from"] == 1443651141
        assert params["date_to"] == 1443661141
        assert params["tags[]"] == ["newsletter"]
        assert "event" not in params
        assert "event[]" not in params
        assert "group_by" not in params
    
    def test_build_query_params_exclude_none_values(self):
        """Test that None values are excluded from query parameters"""
        request = AnalyticsRequest(
            date_from=1443651141,
            date_to=1443661141
            # domain_id is None, tags is None, etc.
        )
        
        params = self.analytics._build_query_params(request)
        
        assert "domain_id" not in params
        assert "tags" not in params
        assert "tags[]" not in params
        assert "recipient_id" not in params
        assert "recipient_id[]" not in params
        assert "event" not in params
        assert "event[]" not in params
    
    def test_build_query_params_array_handling(self):
        """Test handling of array parameters"""
        request = AnalyticsRequest(
            date_from=1443651141,
            date_to=1443661141,
            tags=["tag1", "tag2", "tag3"],
            event=["sent", "delivered", "opened"]
        )
        
        params = self.analytics._build_query_params(request)
        
        # Check that arrays are properly formatted
        assert params["tags[]"] == ["tag1", "tag2", "tag3"]
        assert params["event[]"] == ["sent", "delivered", "opened"]
    
    def test_logging_debug_calls(self):
        """Test that debug logging is called appropriately"""
        # Mock response
        mock_response = Mock(spec=requests.Response)
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": {"stats": []}}
        mock_response.headers = Mock()
        mock_response.headers.get.return_value = "test-request-id"
        mock_response.headers.__iter__ = Mock(return_value=iter(["x-request-id"]))
        mock_response.headers.keys = Mock(return_value=["x-request-id"])
        mock_response.headers.__getitem__ = Mock(return_value="test-request-id")
        mock_response.content = b'{"data": {"stats": []}}'
        
        self.mock_client.request.return_value = mock_response
        
        # Make request
        self.analytics.get_activity_by_date(self.sample_request)
        
        # Check debug logging was called
        self.mock_logger.debug.assert_called()
        self.mock_logger.info.assert_called()
    
    def test_logging_error_calls(self):
        """Test that error occurs for invalid input"""
        # Test with None request
        with pytest.raises(AttributeError):
            self.analytics.get_activity_by_date(None) 