import pytest
from unittest.mock import Mock, patch

from mailersend.resources.sms_sending import SmsSending
from mailersend.models.sms_sending import SmsSendRequest
from mailersend.models.base import APIResponse
from mailersend.exceptions import ValidationError


class TestSmsSendingResource:
    """Test SMS Sending resource."""

    @pytest.fixture
    def mock_client(self):
        """Create a mock client."""
        return Mock()

    @pytest.fixture
    def sms_sending_resource(self, mock_client):
        """Create SMS Sending resource with mock client."""
        return SmsSending(mock_client)

    @pytest.fixture
    def valid_sms_request(self):
        """Create valid SMS request."""
        return SmsSendRequest(
            from_number="+1234567890",
            to=["+1987654321", "+1111111111"],
            text="Hello world!"
        )

    def test_send_success(self, sms_sending_resource, valid_sms_request, mock_client):
        """Test successful SMS sending."""
        # Mock response
        mock_response = Mock()
        mock_response.headers = {
            "X-SMS-Message-Id": "5e42957d51f1d94a1070a733",
            "Content-Type": "text/plain"
        }
        mock_client.request.return_value = mock_response
        
        # Mock _create_response
        expected_response = APIResponse(
            data={},
            headers={"X-SMS-Message-Id": "5e42957d51f1d94a1070a733", "Content-Type": "text/plain"},
            status_code=202
        )
        sms_sending_resource._create_response = Mock(return_value=expected_response)
        
        result = sms_sending_resource.send(valid_sms_request)
        
        # Verify API call
        mock_client.request.assert_called_once_with(
            "POST",
            "sms",
            body={
                "from": "+1234567890",
                "to": ["+1987654321", "+1111111111"],
                "text": "Hello world!"
            }
        )
        
        # Verify response
        assert isinstance(result, APIResponse)
        assert result.status_code == 202

    def test_send_with_personalization(self, sms_sending_resource, mock_client):
        """Test SMS sending with personalization."""
        from mailersend.models.sms_sending import SmsPersonalization
        
        personalization = [
            SmsPersonalization(phone_number="+1987654321", data={"name": "John"})
        ]
        
        request = SmsSendRequest(
            from_number="+1234567890",
            to=["+1987654321"],
            text="Hello {{name}}!",
            personalization=personalization
        )
        
        # Mock response
        mock_response = Mock()
        mock_response.headers = {
            "X-SMS-Message-Id": "5e42957d51f1d94a1070a733"
        }
        mock_client.request.return_value = mock_response
        
        # Mock _create_response
        expected_response = APIResponse(
            data={},
            headers={"X-SMS-Message-Id": "5e42957d51f1d94a1070a733"},
            status_code=202
        )
        sms_sending_resource._create_response = Mock(return_value=expected_response)
        
        result = sms_sending_resource.send(request)
        
        # Verify API call includes personalization
        call_args = mock_client.request.call_args
        assert call_args[0] == ("POST", "sms")
        assert "personalization" in call_args[1]["body"]
        assert len(call_args[1]["body"]["personalization"]) == 1
        assert call_args[1]["body"]["personalization"][0]["phone_number"] == "+1987654321"
        assert call_args[1]["body"]["personalization"][0]["data"]["name"] == "John"

    def test_send_no_request(self, sms_sending_resource):
        """Test sending SMS without request raises validation error."""
        with pytest.raises(ValidationError) as exc_info:
            sms_sending_resource.send(None)
        
        assert "SmsSendRequest must be provided" in str(exc_info.value)

    def test_send_invalid_request_type(self, sms_sending_resource):
        """Test sending SMS with invalid request type raises validation error."""
        with pytest.raises(ValidationError) as exc_info:
            sms_sending_resource.send("invalid-request")
        
        assert "SmsSendRequest must be provided" in str(exc_info.value)

    def test_send_logging(self, sms_sending_resource, valid_sms_request, mock_client):
        """Test that appropriate logging occurs during SMS sending."""
        # Mock response
        mock_response = Mock()
        mock_response.headers = {"X-SMS-Message-Id": "5e42957d51f1d94a1070a733"}
        mock_client.request.return_value = mock_response
        
        # Mock _create_response
        expected_response = APIResponse(
            data={},
            headers={"X-SMS-Message-Id": "5e42957d51f1d94a1070a733"},
            status_code=202
        )
        sms_sending_resource._create_response = Mock(return_value=expected_response)
        
        # Test logging using patch.object
        with patch.object(sms_sending_resource, 'logger') as mock_logger:
            sms_sending_resource.send(valid_sms_request)
            
            # Verify debug logging
            mock_logger.debug.assert_any_call("Preparing to send SMS message")
            
            # Verify info logging
            mock_logger.info.assert_called_with("Sending SMS to 2 recipients")

    def test_send_response_creation(self, sms_sending_resource, valid_sms_request, mock_client):
        """Test that _create_response is called correctly."""
        # Mock response
        mock_response = Mock()
        mock_response.headers = {
            "X-SMS-Message-Id": "test-message-id",
            "Content-Type": "text/plain"
        }
        mock_client.request.return_value = mock_response
        
        # Test that _create_response is called with just the response
        with patch.object(sms_sending_resource, '_create_response') as mock_create_response:
            mock_create_response.return_value = APIResponse(
                data={},
                headers=mock_response.headers,
                status_code=202
            )
            
            result = sms_sending_resource.send(valid_sms_request)
            
            # Verify _create_response was called with only the response
            call_args = mock_create_response.call_args
            assert len(call_args[0]) == 1  # Only one argument
            assert call_args[0][0] == mock_response  # First arg is the response

    def test_send_with_empty_personalization(self, sms_sending_resource, mock_client):
        """Test SMS sending with empty personalization list."""
        request = SmsSendRequest(
            from_number="+1234567890",
            to=["+1987654321"],
            text="Hello world!",
            personalization=[]  # Empty list
        )
        
        # Mock response
        mock_response = Mock()
        mock_response.headers = {"X-SMS-Message-Id": "5e42957d51f1d94a1070a733"}
        mock_client.request.return_value = mock_response
        
        # Mock _create_response
        expected_response = APIResponse(
            data={},
            headers={"X-SMS-Message-Id": "5e42957d51f1d94a1070a733"},
            status_code=202
        )
        sms_sending_resource._create_response = Mock(return_value=expected_response)
        
        result = sms_sending_resource.send(request)
        
        # Verify API call doesn't include personalization
        call_args = mock_client.request.call_args
        assert "personalization" not in call_args[1]["body"]

    def test_send_api_call_format(self, sms_sending_resource, valid_sms_request, mock_client):
        """Test that API call is made with correct format."""
        # Mock response
        mock_response = Mock()
        mock_response.headers = {"X-SMS-Message-Id": "5e42957d51f1d94a1070a733"}
        mock_client.request.return_value = mock_response
        
        # Mock _create_response
        expected_response = APIResponse(data={}, headers={}, status_code=202)
        sms_sending_resource._create_response = Mock(return_value=expected_response)
        
        sms_sending_resource.send(valid_sms_request)
        
        # Verify API call format
        mock_client.request.assert_called_once_with(
            "POST",
            "sms",
            body={
                "from": "+1234567890",
                "to": ["+1987654321", "+1111111111"],
                "text": "Hello world!"
            }
        )