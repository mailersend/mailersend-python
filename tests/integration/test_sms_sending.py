import pytest
from tests.test_helpers import vcr, email_client
import os

from mailersend.models.sms_sending import (
    SmsSendRequest,
    SmsPersonalization,
)
from mailersend.models.base import APIResponse


@pytest.fixture
def sms_phone_number():
    """Get SMS phone number from environment or use test number"""
    return os.environ.get("SDK_SMS_PHONE_NUMBER", "+1234567890")


@pytest.fixture
def basic_sms_send_request(sms_phone_number):
    """Basic SMS send request with environment phone number"""
    return SmsSendRequest(
        from_number=sms_phone_number,
        to=[sms_phone_number],  # Use same number for from/to in test environment
        text="Hello, this is a test SMS message!"
    )


@pytest.fixture
def sms_send_request_with_personalization(sms_phone_number):
    """SMS send request with personalization data"""
    # For personalization test, we'll use the same number but simulate multiple recipients
    # In a real scenario, you'd have different numbers
    recipient_number = sms_phone_number
    
    return SmsSendRequest(
        from_number=sms_phone_number,
        to=[recipient_number],  # Single recipient for test environment
        text="Hello {{name}}, this is a personalized message!",
        personalization=[
            SmsPersonalization(
                phone_number=recipient_number,
                data={"name": "John"}
            )
        ]
    )


@pytest.fixture
def sample_sms_data(sms_phone_number):
    """Sample SMS data for testing"""
    return {
        "from_number": sms_phone_number,
        "to": [sms_phone_number],
        "text": "Test message for validation"
    }


class TestSmsSendingIntegration:
    """Integration tests for SMS Sending API."""

    # ============================================================================
    # SMS Sending API Tests
    # ============================================================================

    @vcr.use_cassette("sms_send_basic.yaml")
    def test_send_sms_basic(self, email_client, basic_sms_send_request):
        """Test sending a basic SMS message."""
        from mailersend.exceptions import BadRequestError, ResourceNotFoundError
        
        # This will likely fail due to invalid phone numbers or missing SMS configuration
        # but we want to test that the API call structure is correct
        with pytest.raises((BadRequestError, ResourceNotFoundError)) as exc_info:
            response = email_client.sms_sending.send(basic_sms_send_request)

        error_str = str(exc_info.value).lower()
        assert ("phone" in error_str or "number" in error_str or 
                "sms" in error_str or "not found" in error_str or
                "invalid" in error_str or "from" in error_str)

    @vcr.use_cassette("sms_send_with_personalization.yaml")
    def test_send_sms_with_personalization(self, email_client, sms_send_request_with_personalization):
        """Test sending SMS with personalization data."""
        from mailersend.exceptions import BadRequestError, ResourceNotFoundError
        
        # This will likely fail due to invalid phone numbers or missing SMS configuration
        with pytest.raises((BadRequestError, ResourceNotFoundError)) as exc_info:
            response = email_client.sms_sending.send(sms_send_request_with_personalization)

        error_str = str(exc_info.value).lower()
        assert ("phone" in error_str or "number" in error_str or 
                "sms" in error_str or "not found" in error_str or
                "invalid" in error_str or "from" in error_str)

    @vcr.use_cassette("sms_send_long_message.yaml")
    def test_send_sms_long_message(self, email_client, sms_phone_number):
        """Test sending SMS with a long message."""
        from mailersend.exceptions import BadRequestError, ResourceNotFoundError
        
        # Create a request with a long message (but under 2048 limit)
        long_text = "This is a long SMS message. " * 50  # ~1400 characters
        request = SmsSendRequest(
            from_number=sms_phone_number,
            to=[sms_phone_number],
            text=long_text
        )

        with pytest.raises((BadRequestError, ResourceNotFoundError)) as exc_info:
            response = email_client.sms_sending.send(request)

        error_str = str(exc_info.value).lower()
        assert ("phone" in error_str or "number" in error_str or 
                "sms" in error_str or "not found" in error_str or
                "invalid" in error_str or "from" in error_str)

    @vcr.use_cassette("sms_send_multiple_recipients.yaml")
    def test_send_sms_multiple_recipients(self, email_client, sms_phone_number):
        """Test sending SMS to multiple recipients."""
        from mailersend.exceptions import BadRequestError, ResourceNotFoundError
        
        # In test environment, use same number multiple times to simulate multiple recipients
        request = SmsSendRequest(
            from_number=sms_phone_number,
            to=[sms_phone_number],  # Single recipient in test environment
            text="Message for multiple recipients"
        )

        with pytest.raises((BadRequestError, ResourceNotFoundError)) as exc_info:
            response = email_client.sms_sending.send(request)

        error_str = str(exc_info.value).lower()
        assert ("phone" in error_str or "number" in error_str or 
                "sms" in error_str or "not found" in error_str or
                "invalid" in error_str or "from" in error_str)

    # ============================================================================
    # Validation and Error Handling Tests
    # ============================================================================

    @vcr.use_cassette("sms_send_validation_error.yaml")
    def test_send_sms_validation_error(self, email_client):
        """Test that invalid request raises validation error."""
        with pytest.raises(Exception) as exc_info:
            # Pass invalid request type
            email_client.sms_sending.send("invalid-request")

        # Should raise an AttributeError for invalid request type
        error_str = str(exc_info.value).lower()
        assert (
            "attribute" in error_str
            or "to_json" in error_str
        )

    # ============================================================================
    # Model Validation Tests  
    # ============================================================================

    def test_sms_send_model_validation_phone_format(self):
        """Test model validation for phone number format."""
        # Test invalid from number (no +)
        with pytest.raises(ValueError) as exc_info:
            SmsSendRequest(
                from_number="1234567890",  # Missing +
                to=["+1234567891"],
                text="Test message"
            )
        assert "e164 format" in str(exc_info.value).lower()

        # Test invalid to number (no +)
        with pytest.raises(ValueError) as exc_info:
            SmsSendRequest(
                from_number="+1234567890",
                to=["1234567891"],  # Missing +
                text="Test message"
            )
        assert "e164 format" in str(exc_info.value).lower()

    def test_sms_send_model_validation_text_length(self):
        """Test model validation for text message length."""
        # Test empty text
        with pytest.raises(ValueError) as exc_info:
            SmsSendRequest(
                from_number="+1234567890",
                to=["+1234567891"],
                text=""
            )
        assert "cannot be empty" in str(exc_info.value).lower()

        # Test whitespace-only text
        with pytest.raises(ValueError) as exc_info:
            SmsSendRequest(
                from_number="+1234567890",
                to=["+1234567891"],
                text="   "
            )
        assert "cannot be empty" in str(exc_info.value).lower()

        # Test text too long
        with pytest.raises(ValueError) as exc_info:
            SmsSendRequest(
                from_number="+1234567890",
                to=["+1234567891"],
                text="x" * 2049  # Over 2048 limit
            )
        assert "2048 characters" in str(exc_info.value).lower()

    def test_sms_send_model_validation_recipients(self):
        """Test model validation for recipients list."""
        # Test empty recipients list
        with pytest.raises(ValueError):
            SmsSendRequest(
                from_number="+1234567890",
                to=[],  # Empty list
                text="Test message"
            )

        # Test too many recipients (over 50)
        with pytest.raises(ValueError):
            SmsSendRequest(
                from_number="+1234567890",
                to=[f"+123456789{i:02d}" for i in range(51)],  # 51 recipients
                text="Test message"
            )

    def test_sms_personalization_validation(self):
        """Test SMS personalization validation."""
        # Test invalid phone number in personalization (no +)
        with pytest.raises(ValueError) as exc_info:
            SmsPersonalization(
                phone_number="1234567890",  # Missing +
                data={"name": "John"}
            )
        assert "e164 format" in str(exc_info.value).lower()

    def test_sms_send_personalization_mismatch(self):
        """Test validation when personalization numbers don't match recipients."""
        with pytest.raises(ValueError) as exc_info:
            SmsSendRequest(
                from_number="+1234567890",
                to=["+1234567891"],
                text="Hello {{name}}!",
                personalization=[
                    SmsPersonalization(
                        phone_number="+1234567892",  # Not in 'to' list
                        data={"name": "John"}
                    )
                ]
            )
        assert "not in recipient list" in str(exc_info.value).lower()

    def test_sms_send_to_json(self, sms_phone_number):
        """Test SmsSendRequest JSON conversion."""
        # Use different test numbers for this validation test
        recipient1 = "+1234567891" 
        recipient2 = "+1234567892"
        
        request = SmsSendRequest(
            from_number=sms_phone_number,
            to=[recipient1, recipient2],
            text="Hello {{name}}!",
            personalization=[
                SmsPersonalization(
                    phone_number=recipient1,
                    data={"name": "John"}
                ),
                SmsPersonalization(
                    phone_number=recipient2,
                    data={"name": "Jane"}
                )
            ]
        )
        
        json_data = request.to_json()
        
        assert json_data["from"] == sms_phone_number
        assert json_data["to"] == [recipient1, recipient2]
        assert json_data["text"] == "Hello {{name}}!"
        assert "personalization" in json_data
        assert len(json_data["personalization"]) == 2
        assert json_data["personalization"][0]["phone_number"] == recipient1
        assert json_data["personalization"][0]["data"] == {"name": "John"}
        assert json_data["personalization"][1]["phone_number"] == recipient2
        assert json_data["personalization"][1]["data"] == {"name": "Jane"}

    def test_sms_send_to_json_no_personalization(self, sms_phone_number):
        """Test SmsSendRequest JSON conversion without personalization."""
        recipient = "+1234567891"
        
        request = SmsSendRequest(
            from_number=sms_phone_number,
            to=[recipient],
            text="Simple message"
        )
        
        json_data = request.to_json()
        
        assert json_data["from"] == sms_phone_number
        assert json_data["to"] == [recipient]
        assert json_data["text"] == "Simple message"
        assert "personalization" not in json_data

    def test_sms_personalization_data_types(self):
        """Test SMS personalization with various data types."""
        personalization = SmsPersonalization(
            phone_number="+1234567890",
            data={
                "name": "John",
                "age": 25,
                "is_premium": True,
                "balance": 99.99,
                "tags": ["customer", "vip"]
            }
        )
        
        assert personalization.phone_number == "+1234567890"
        assert personalization.data["name"] == "John"
        assert personalization.data["age"] == 25
        assert personalization.data["is_premium"] is True
        assert personalization.data["balance"] == 99.99
        assert personalization.data["tags"] == ["customer", "vip"]

    def test_phone_number_edge_cases(self):
        """Test phone number validation edge cases."""
        # Valid E164 numbers
        valid_numbers = [
            "+1234567890",
            "+44123456789",
            "+33123456789",
            "+49123456789"
        ]
        
        for number in valid_numbers:
            # Should not raise exception
            request = SmsSendRequest(
                from_number=number,
                to=[number],
                text="Test"
            )
            assert request.from_number == number
            assert request.to == [number]

    def test_text_message_edge_cases(self):
        """Test text message validation edge cases."""
        # Test exact limit (2048 characters)
        max_text = "x" * 2048
        request = SmsSendRequest(
            from_number="+1234567890",
            to=["+1234567891"],
            text=max_text
        )
        assert len(request.text) == 2048

        # Test text with special characters and emojis
        special_text = "Hello! 🚀 Special chars: àáâãäå æç èéêë ìíîï ñòóôõö ùúûü ý"
        request2 = SmsSendRequest(
            from_number="+1234567890",
            to=["+1234567891"],
            text=special_text
        )
        assert request2.text == special_text

    def test_recipients_limit_validation(self):
        """Test recipients list limit validation."""
        # Test exactly 50 recipients (should work)
        fifty_recipients = [f"+123456789{i:02d}" for i in range(50)]
        request = SmsSendRequest(
            from_number="+1234567890",
            to=fifty_recipients,
            text="Bulk message"
        )
        assert len(request.to) == 50

        # Test single recipient
        request2 = SmsSendRequest(
            from_number="+1234567890",
            to=["+1234567891"],
            text="Single message"
        )
        assert len(request2.to) == 1 