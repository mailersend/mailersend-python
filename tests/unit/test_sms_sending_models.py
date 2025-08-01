"""Unit tests for SMS Sending models."""

import pytest
from pydantic import ValidationError

from mailersend.models.sms_sending import (
    SmsPersonalization,
    SmsSendRequest,
)


class TestSmsPersonalization:
    """Test SmsPersonalization model."""

    def test_valid_personalization(self):
        """Test creating valid personalization."""
        personalization = SmsPersonalization(
            phone_number="+1234567890", data={"name": "John", "city": "New York"}
        )

        assert personalization.phone_number == "+1234567890"
        assert personalization.data == {"name": "John", "city": "New York"}

    def test_phone_number_validation(self):
        """Test phone number validation."""
        with pytest.raises(ValueError, match="Phone number must be in E164 format"):
            SmsPersonalization(
                phone_number="1234567890", data={"name": "John"}  # Missing +
            )

    def test_empty_data(self):
        """Test personalization with empty data."""
        personalization = SmsPersonalization(phone_number="+1234567890", data={})
        assert personalization.data == {}


class TestSmsSendRequest:
    """Test SmsSendRequest model."""

    def test_valid_request(self):
        """Test creating valid SMS send request."""
        request = SmsSendRequest(
            from_number="+1234567890",
            to=["+1987654321", "+1111111111"],
            text="Hello world!",
        )

        assert request.from_number == "+1234567890"
        assert request.to == ["+1987654321", "+1111111111"]
        assert request.text == "Hello world!"
        assert request.personalization is None

    def test_request_with_personalization(self):
        """Test request with personalization."""
        personalization = [
            SmsPersonalization(phone_number="+1987654321", data={"name": "John"}),
            SmsPersonalization(phone_number="+1111111111", data={"name": "Jane"}),
        ]

        request = SmsSendRequest(
            from_number="+1234567890",
            to=["+1987654321", "+1111111111"],
            text="Hello {{name}}!",
            personalization=personalization,
        )

        assert len(request.personalization) == 2
        assert request.personalization[0].phone_number == "+1987654321"
        assert request.personalization[1].data["name"] == "Jane"

    def test_from_number_validation(self):
        """Test from number validation."""
        with pytest.raises(ValueError, match="From number must be in E164 format"):
            SmsSendRequest(
                from_number="1234567890", to=["+1987654321"], text="Hello!"  # Missing +
            )

    def test_to_numbers_validation(self):
        """Test to numbers validation."""
        with pytest.raises(
            ValueError, match="All phone numbers must be in E164 format"
        ):
            SmsSendRequest(
                from_number="+1234567890", to=["1987654321"], text="Hello!"  # Missing +
            )

    def test_text_length_validation(self):
        """Test text length validation."""
        long_text = "x" * 2049  # Exceeds 2048 character limit
        with pytest.raises(ValidationError):
            SmsSendRequest(
                from_number="+1234567890", to=["+1987654321"], text=long_text
            )

    def test_empty_text_validation(self):
        """Test empty text validation."""
        with pytest.raises(ValueError, match="Text message cannot be empty"):
            SmsSendRequest(
                from_number="+1234567890",
                to=["+1987654321"],
                text="   ",  # Only whitespace
            )

    def test_empty_to_list_validation(self):
        """Test empty to list validation."""
        with pytest.raises(ValidationError):
            SmsSendRequest(
                from_number="+1234567890", to=[], text="Hello!"  # Empty list
            )

    def test_too_many_recipients_validation(self):
        """Test too many recipients validation."""
        recipients = [f"+{i:010d}" for i in range(51)]  # 51 recipients (over limit)
        with pytest.raises(ValidationError):
            SmsSendRequest(from_number="+1234567890", to=recipients, text="Hello!")

    def test_personalization_validation_invalid_numbers(self):
        """Test personalization validation with invalid phone numbers."""
        personalization = [
            SmsPersonalization(phone_number="+1555555555", data={"name": "John"})
        ]

        with pytest.raises(
            ValueError, match="Personalization phone numbers not in recipient list"
        ):
            SmsSendRequest(
                from_number="+1234567890",
                to=["+1987654321"],  # Different number than in personalization
                text="Hello {{name}}!",
                personalization=personalization,
            )

    def test_to_json_basic(self):
        """Test converting to JSON without personalization."""
        request = SmsSendRequest(
            from_number="+1234567890",
            to=["+1987654321", "+1111111111"],
            text="Hello world!",
        )

        json_data = request.to_json()
        expected = {
            "from": "+1234567890",
            "to": ["+1987654321", "+1111111111"],
            "text": "Hello world!",
        }
        assert json_data == expected

    def test_to_json_with_personalization(self):
        """Test converting to JSON with personalization."""
        personalization = [
            SmsPersonalization(phone_number="+1987654321", data={"name": "John"}),
            SmsPersonalization(phone_number="+1111111111", data={"name": "Jane"}),
        ]

        request = SmsSendRequest(
            from_number="+1234567890",
            to=["+1987654321", "+1111111111"],
            text="Hello {{name}}!",
            personalization=personalization,
        )

        json_data = request.to_json()
        expected = {
            "from": "+1234567890",
            "to": ["+1987654321", "+1111111111"],
            "text": "Hello {{name}}!",
            "personalization": [
                {"phone_number": "+1987654321", "data": {"name": "John"}},
                {"phone_number": "+1111111111", "data": {"name": "Jane"}},
            ],
        }
        assert json_data == expected

    def test_model_validation_with_alias(self):
        """Test model validation with field alias."""
        data = {
            "from": "+1234567890",  # Using alias
            "to": ["+1987654321"],
            "text": "Hello!",
        }

        request = SmsSendRequest(**data)
        assert request.from_number == "+1234567890"
