import pytest

from mailersend.builders.sms_sending import SmsSendingBuilder
from mailersend.models.sms_sending import SmsSendRequest, SmsPersonalization


class TestSmsSendingBuilder:
    """Test SMS Sending builder."""

    @pytest.fixture
    def builder(self):
        """Create a fresh builder instance."""
        return SmsSendingBuilder()

    def test_basic_sms_building(self, builder):
        """Test building a basic SMS request."""
        request = (builder
                  .from_number("+1234567890")
                  .to(["+1987654321", "+1111111111"])
                  .text("Hello world!")
                  .build())
        
        assert isinstance(request, SmsSendRequest)
        assert request.from_number == "+1234567890"
        assert request.to == ["+1987654321", "+1111111111"]
        assert request.text == "Hello world!"
        assert request.personalization is None

    def test_sms_with_single_recipient(self, builder):
        """Test building SMS with single recipient."""
        request = (builder
                  .from_number("+1234567890")
                  .add_recipient("+1987654321")
                  .text("Hello world!")
                  .build())
        
        assert request.to == ["+1987654321"]

    def test_sms_with_multiple_recipients_added_individually(self, builder):
        """Test building SMS with multiple recipients added individually."""
        request = (builder
                  .from_number("+1234567890")
                  .add_recipient("+1987654321")
                  .add_recipient("+1111111111")
                  .add_recipient("+1222222222")
                  .text("Hello world!")
                  .build())
        
        assert request.to == ["+1987654321", "+1111111111", "+1222222222"]

    def test_sms_with_duplicate_recipients(self, builder):
        """Test that duplicate recipients are not added."""
        request = (builder
                  .from_number("+1234567890")
                  .add_recipient("+1987654321")
                  .add_recipient("+1987654321")  # Duplicate
                  .text("Hello world!")
                  .build())
        
        assert request.to == ["+1987654321"]

    def test_sms_with_personalization_list(self, builder):
        """Test building SMS with personalization list."""
        personalizations = [
            SmsPersonalization(phone_number="+1987654321", data={"name": "John"}),
            SmsPersonalization(phone_number="+1111111111", data={"name": "Jane"})
        ]
        
        request = (builder
                  .from_number("+1234567890")
                  .to(["+1987654321", "+1111111111"])
                  .text("Hello {{name}}!")
                  .personalization(personalizations)
                  .build())
        
        assert len(request.personalization) == 2
        assert request.personalization[0].phone_number == "+1987654321"
        assert request.personalization[0].data == {"name": "John"}
        assert request.personalization[1].phone_number == "+1111111111"
        assert request.personalization[1].data == {"name": "Jane"}

    def test_sms_with_added_personalization(self, builder):
        """Test building SMS with individually added personalization."""
        request = (builder
                  .from_number("+1234567890")
                  .to(["+1987654321", "+1111111111"])
                  .text("Hello {{name}}!")
                  .add_personalization("+1987654321", {"name": "John"})
                  .add_personalization("+1111111111", {"name": "Jane"})
                  .build())
        
        assert len(request.personalization) == 2
        assert request.personalization[0].phone_number == "+1987654321"
        assert request.personalization[0].data == {"name": "John"}
        assert request.personalization[1].phone_number == "+1111111111"
        assert request.personalization[1].data == {"name": "Jane"}

    def test_sms_with_complex_personalization_data(self, builder):
        """Test building SMS with complex personalization data."""
        request = (builder
                  .from_number("+1234567890")
                  .to(["+1987654321"])
                  .text("Hello {{name}}! Your order {{order_id}} is {{status}}.")
                  .add_personalization("+1987654321", {
                      "name": "John",
                      "order_id": "12345",
                      "status": "shipped",
                      "amount": 99.99
                  })
                  .build())
        
        assert len(request.personalization) == 1
        assert request.personalization[0].data == {
            "name": "John",
            "order_id": "12345",
            "status": "shipped",
            "amount": 99.99
        }

    def test_build_missing_from_number(self, builder):
        """Test building SMS without from number raises error."""
        with pytest.raises(ValueError) as exc_info:
            (builder
             .to(["+1987654321"])
             .text("Hello world!")
             .build())
        
        assert "From number is required" in str(exc_info.value)

    def test_build_missing_recipients(self, builder):
        """Test building SMS without recipients raises error."""
        with pytest.raises(ValueError) as exc_info:
            (builder
             .from_number("+1234567890")
             .text("Hello world!")
             .build())
        
        assert "At least one recipient is required" in str(exc_info.value)

    def test_build_missing_text(self, builder):
        """Test building SMS without text raises error."""
        with pytest.raises(ValueError) as exc_info:
            (builder
             .from_number("+1234567890")
             .to(["+1987654321"])
             .build())
        
        assert "Text message is required" in str(exc_info.value)

    def test_builder_method_chaining(self, builder):
        """Test that all builder methods return self for chaining."""
        assert builder.from_number("+1234567890") is builder
        assert builder.to(["+1987654321"]) is builder
        assert builder.add_recipient("+1111111111") is builder
        assert builder.text("Hello world!") is builder
        assert builder.personalization([]) is builder
        assert builder.add_personalization("+1987654321", {"name": "John"}) is builder
        assert builder.clear() is builder

    def test_builder_clear(self, builder):
        """Test clearing builder values."""
        # Set some values
        builder.from_number("+1234567890")
        builder.to(["+1987654321"])
        builder.text("Hello world!")
        builder.add_personalization("+1987654321", {"name": "John"})
        
        # Clear and verify
        builder.clear()
        
        with pytest.raises(ValueError):
            builder.build()  # Should fail because all values are cleared

    def test_builder_reuse_after_clear(self, builder):
        """Test that builder can be reused after clearing."""
        # Build first SMS
        request1 = (builder
                   .from_number("+1234567890")
                   .to(["+1987654321"])
                   .text("Hello world!")
                   .build())
        
        # Clear and build second SMS
        request2 = (builder
                   .clear()
                   .from_number("+1111111111")
                   .to(["+1222222222"])
                   .text("Goodbye world!")
                   .build())
        
        # Verify both are different
        assert request1.from_number != request2.from_number
        assert request1.to != request2.to
        assert request1.text != request2.text

    def test_builder_with_mixed_recipient_methods(self, builder):
        """Test using both to() and add_recipient() methods."""
        request = (builder
                  .from_number("+1234567890")
                  .to(["+1987654321", "+1111111111"])
                  .add_recipient("+1222222222")
                  .text("Hello world!")
                  .build())
        
        assert request.to == ["+1987654321", "+1111111111", "+1222222222"]

    def test_builder_overwrite_values(self, builder):
        """Test that builder methods overwrite previous values."""
        request = (builder
                  .from_number("+1234567890")
                  .from_number("+1111111111")  # Overwrite
                  .to(["+1987654321"])
                  .to(["+1222222222"])  # Overwrite
                  .text("Hello world!")
                  .text("Goodbye world!")  # Overwrite
                  .build())
        
        assert request.from_number == "+1111111111"
        assert request.to == ["+1222222222"]
        assert request.text == "Goodbye world!"

    def test_builder_empty_personalization_list(self, builder):
        """Test building SMS with empty personalization list."""
        request = (builder
                  .from_number("+1234567890")
                  .to(["+1987654321"])
                  .text("Hello world!")
                  .personalization([])  # Empty list
                  .build())
        
        assert request.personalization is None

    def test_builder_with_long_message(self, builder):
        """Test building SMS with maximum length message."""
        long_message = "x" * 2048  # Maximum length
        
        request = (builder
                  .from_number("+1234567890")
                  .to(["+1987654321"])
                  .text(long_message)
                  .build())
        
        assert len(request.text) == 2048
        assert request.text == long_message