import pytest
from pydantic import ValidationError

from mailersend.models.sms_sending import (
    SmsPersonalization, SmsSendRequest, SmsSendResponse
)


class TestSmsPersonalization:
    """Test SMS personalization model."""

    def test_valid_personalization(self):
        """Test creating valid personalization."""
        personalization = SmsPersonalization(
            phone_number="+1234567890",
            data={"name": "John", "order_id": "12345"}
        )
        
        assert personalization.phone_number == "+1234567890"
        assert personalization.data == {"name": "John", "order_id": "12345"}

    def test_invalid_phone_number_format(self):
        """Test validation error for invalid phone number format."""
        with pytest.raises(ValidationError) as exc_info:
            SmsPersonalization(
                phone_number="1234567890",  # Missing +
                data={"name": "John"}
            )
        
        error = exc_info.value.errors()[0]
        assert "Phone number must be in E164 format" in error['msg']

    def test_empty_data(self):
        """Test personalization with empty data."""
        personalization = SmsPersonalization(
            phone_number="+1234567890",
            data={}
        )
        
        assert personalization.data == {}


class TestSmsSendRequest:
    """Test SMS send request model."""

    def test_valid_sms_request(self):
        """Test creating valid SMS request."""
        request = SmsSendRequest(
            from_number="+1234567890",
            to=["+1987654321", "+1111111111"],
            text="Hello world!"
        )
        
        assert request.from_number == "+1234567890"
        assert request.to == ["+1987654321", "+1111111111"]
        assert request.text == "Hello world!"
        assert request.personalization is None

    def test_valid_sms_request_with_personalization(self):
        """Test creating valid SMS request with personalization."""
        personalization = [
            SmsPersonalization(phone_number="+1987654321", data={"name": "John"}),
            SmsPersonalization(phone_number="+1111111111", data={"name": "Jane"})
        ]
        
        request = SmsSendRequest(
            from_number="+1234567890",
            to=["+1987654321", "+1111111111"],
            text="Hello {{name}}!",
            personalization=personalization
        )
        
        assert len(request.personalization) == 2
        assert request.personalization[0].phone_number == "+1987654321"
        assert request.personalization[0].data == {"name": "John"}

    def test_invalid_from_number(self):
        """Test validation error for invalid from number."""
        with pytest.raises(ValidationError) as exc_info:
            SmsSendRequest(
                from_number="1234567890",  # Missing +
                to=["+1987654321"],
                text="Hello world!"
            )
        
        error = exc_info.value.errors()[0]
        assert "From number must be in E164 format" in error['msg']

    def test_invalid_to_numbers(self):
        """Test validation error for invalid to numbers."""
        with pytest.raises(ValidationError) as exc_info:
            SmsSendRequest(
                from_number="+1234567890",
                to=["1987654321"],  # Missing +
                text="Hello world!"
            )
        
        error = exc_info.value.errors()[0]
        assert "All phone numbers must be in E164 format" in error['msg']

    def test_empty_to_list(self):
        """Test validation error for empty to list."""
        with pytest.raises(ValidationError) as exc_info:
            SmsSendRequest(
                from_number="+1234567890",
                to=[],
                text="Hello world!"
            )
        
        error = exc_info.value.errors()[0]
        assert "at least 1 item" in error['msg']

    def test_too_many_recipients(self):
        """Test validation error for too many recipients."""
        with pytest.raises(ValidationError) as exc_info:
            SmsSendRequest(
                from_number="+1234567890",
                to=[f"+{i:010d}" for i in range(51)],  # 51 recipients
                text="Hello world!"
            )
        
        error = exc_info.value.errors()[0]
        assert "at most 50 items" in error['msg']

    def test_empty_text(self):
        """Test validation error for empty text."""
        with pytest.raises(ValidationError) as exc_info:
            SmsSendRequest(
                from_number="+1234567890",
                to=["+1987654321"],
                text=""
            )
        
        error = exc_info.value.errors()[0]
        assert "Text message cannot be empty" in error['msg']

    def test_text_too_long(self):
        """Test validation error for text too long."""
        with pytest.raises(ValidationError) as exc_info:
            SmsSendRequest(
                from_number="+1234567890",
                to=["+1987654321"],
                text="x" * 2049  # 2049 characters
            )
        
        error = exc_info.value.errors()[0]
        assert "String should have at most 2048 characters" in error['msg']

    def test_personalization_phone_not_in_to_list(self):
        """Test validation error for personalization phone not in to list."""
        personalization = [
            SmsPersonalization(phone_number="+1555555555", data={"name": "John"})
        ]
        
        with pytest.raises(ValidationError) as exc_info:
            SmsSendRequest(
                from_number="+1234567890",
                to=["+1987654321"],
                text="Hello {{name}}!",
                personalization=personalization
            )
        
        error = exc_info.value.errors()[0]
        assert "Personalization phone numbers not in recipient list" in error['msg']

    def test_to_json_basic(self):
        """Test converting basic request to JSON."""
        request = SmsSendRequest(
            from_number="+1234567890",
            to=["+1987654321", "+1111111111"],
            text="Hello world!"
        )
        
        json_data = request.to_json()
        expected = {
            "from": "+1234567890",
            "to": ["+1987654321", "+1111111111"],
            "text": "Hello world!"
        }
        
        assert json_data == expected

    def test_to_json_with_personalization(self):
        """Test converting request with personalization to JSON."""
        personalization = [
            SmsPersonalization(phone_number="+1987654321", data={"name": "John"}),
            SmsPersonalization(phone_number="+1111111111", data={"name": "Jane"})
        ]
        
        request = SmsSendRequest(
            from_number="+1234567890",
            to=["+1987654321", "+1111111111"],
            text="Hello {{name}}!",
            personalization=personalization
        )
        
        json_data = request.to_json()
        expected = {
            "from": "+1234567890",
            "to": ["+1987654321", "+1111111111"],
            "text": "Hello {{name}}!",
            "personalization": [
                {"phone_number": "+1987654321", "data": {"name": "John"}},
                {"phone_number": "+1111111111", "data": {"name": "Jane"}}
            ]
        }
        
        assert json_data == expected

    def test_field_aliases(self):
        """Test that field aliases work correctly."""
        # Test using alias in dict
        data = {
            "from": "+1234567890",
            "to": ["+1987654321"],
            "text": "Hello world!"
        }
        
        request = SmsSendRequest(**data)
        assert request.from_number == "+1234567890"


class TestSmsSendResponse:
    """Test SMS send response model."""

    def test_default_values(self):
        """Test default response values."""
        response = SmsSendResponse()
        
        assert response.message_id is None
        assert response.send_paused is False
        assert response.status == "queued"

    def test_from_headers_basic(self):
        """Test creating response from headers."""
        headers = {
            "X-SMS-Message-Id": "5e42957d51f1d94a1070a733",
            "Content-Type": "text/plain"
        }
        
        response = SmsSendResponse.from_headers(headers)
        
        assert response.message_id == "5e42957d51f1d94a1070a733"
        assert response.send_paused is False
        assert response.status == "queued"

    def test_from_headers_paused(self):
        """Test creating response from headers with paused status."""
        headers = {
            "X-SMS-Message-Id": "5e42957d51f1d94a1070a733",
            "X-SMS-Send-Paused": "true",
            "Content-Type": "text/plain"
        }
        
        response = SmsSendResponse.from_headers(headers)
        
        assert response.message_id == "5e42957d51f1d94a1070a733"
        assert response.send_paused is True
        assert response.status == "paused"

    def test_from_headers_missing_id(self):
        """Test creating response from headers without message ID."""
        headers = {
            "Content-Type": "text/plain"
        }
        
        response = SmsSendResponse.from_headers(headers)
        
        assert response.message_id is None
        assert response.send_paused is False
        assert response.status == "queued"

    def test_from_headers_case_insensitive_paused(self):
        """Test paused header is case insensitive."""
        headers = {
            "X-SMS-Message-Id": "5e42957d51f1d94a1070a733",
            "X-SMS-Send-Paused": "True",
            "Content-Type": "text/plain"
        }
        
        response = SmsSendResponse.from_headers(headers)
        
        assert response.send_paused is True
        assert response.status == "paused"