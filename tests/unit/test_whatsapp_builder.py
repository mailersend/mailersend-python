import pytest

from mailersend.builders.whatsapp import WhatsAppBuilder
from mailersend.models.whatsapp import (
    WhatsAppPersonalization,
    WhatsAppPersonalizationData,
    WhatsAppSendRequest,
)


class TestWhatsAppBuilder:
    """Test WhatsApp builder."""

    @pytest.fixture
    def builder(self):
        """Create a fresh builder instance."""
        return WhatsAppBuilder()

    def test_basic_build(self, builder):
        """Test building a basic WhatsApp request."""
        request = (
            builder.from_number("12345678901")
            .add_recipient("19191234567")
            .template_id("abc123")
            .build()
        )

        assert isinstance(request, WhatsAppSendRequest)
        assert request.from_number == "12345678901"
        assert request.to == ["19191234567"]
        assert request.template_id == "abc123"
        assert request.personalization is None

    def test_build_with_multiple_recipients(self, builder):
        """Test building request with multiple recipients."""
        request = (
            builder.from_number("12345678901")
            .to(["19191234567", "19199876543"])
            .template_id("abc123")
            .build()
        )

        assert request.to == ["19191234567", "19199876543"]

    def test_build_with_duplicate_recipients(self, builder):
        """Test that duplicate recipients are not added."""
        request = (
            builder.from_number("12345678901")
            .add_recipient("19191234567")
            .add_recipient("19191234567")
            .template_id("abc123")
            .build()
        )

        assert request.to == ["19191234567"]

    def test_build_with_personalization(self, builder):
        """Test building request with personalization."""
        personalization = WhatsAppPersonalization(
            to="19191234567",
            data=WhatsAppPersonalizationData(
                header=["John"],
                body=["order #1234", "tomorrow"],
                buttons=["https://example.com/track/1234"],
            ),
        )

        request = (
            builder.from_number("12345678901")
            .add_recipient("19191234567")
            .template_id("abc123")
            .add_personalization(personalization)
            .build()
        )

        assert len(request.personalization) == 1
        assert request.personalization[0].to == "19191234567"
        assert request.personalization[0].data.header == ["John"]
        assert request.personalization[0].data.body == ["order #1234", "tomorrow"]
        assert request.personalization[0].data.buttons == ["https://example.com/track/1234"]

    def test_build_missing_from_number(self, builder):
        """Test building without from number raises error."""
        with pytest.raises(ValueError) as exc_info:
            builder.add_recipient("19191234567").template_id("abc123").build()

        assert "From number is required" in str(exc_info.value)

    def test_build_missing_recipients(self, builder):
        """Test building without recipients raises error."""
        with pytest.raises(ValueError) as exc_info:
            builder.from_number("12345678901").template_id("abc123").build()

        assert "At least one recipient is required" in str(exc_info.value)

    def test_build_missing_template_id(self, builder):
        """Test building without template ID raises error."""
        with pytest.raises(ValueError) as exc_info:
            builder.from_number("12345678901").add_recipient("19191234567").build()

        assert "Template ID is required" in str(exc_info.value)

    def test_builder_method_chaining(self, builder):
        """Test that all builder methods return self for chaining."""
        personalization = WhatsAppPersonalization(
            to="19191234567",
            data=WhatsAppPersonalizationData(),
        )
        assert builder.from_number("12345678901") is builder
        assert builder.to(["19191234567"]) is builder
        assert builder.add_recipient("19199876543") is builder
        assert builder.template_id("abc123") is builder
        assert builder.add_personalization(personalization) is builder
        assert builder.clear() is builder

    def test_builder_clear(self, builder):
        """Test clearing builder values."""
        builder.from_number("12345678901")
        builder.add_recipient("19191234567")
        builder.template_id("abc123")

        builder.clear()

        with pytest.raises(ValueError):
            builder.build()

    def test_builder_reuse_after_clear(self, builder):
        """Test that builder can be reused after clearing."""
        request1 = (
            builder.from_number("12345678901")
            .add_recipient("19191234567")
            .template_id("template1")
            .build()
        )

        request2 = (
            builder.clear()
            .from_number("19998887777")
            .add_recipient("19199876543")
            .template_id("template2")
            .build()
        )

        assert request1.from_number != request2.from_number
        assert request1.to != request2.to
        assert request1.template_id != request2.template_id

    def test_to_json_basic(self, builder):
        """Test to_json produces correct output for basic request."""
        request = (
            builder.from_number("12345678901")
            .add_recipient("19191234567")
            .template_id("abc123")
            .build()
        )

        json_data = request.to_json()

        assert json_data == {
            "from": "12345678901",
            "to": ["19191234567"],
            "template_id": "abc123",
        }

    def test_to_json_with_personalization(self, builder):
        """Test to_json produces correct output with personalization."""
        personalization = WhatsAppPersonalization(
            to="19191234567",
            data=WhatsAppPersonalizationData(
                header=["John"],
                body=["order #1234"],
            ),
        )

        request = (
            builder.from_number("12345678901")
            .add_recipient("19191234567")
            .template_id("abc123")
            .add_personalization(personalization)
            .build()
        )

        json_data = request.to_json()

        assert json_data["personalization"] == [
            {
                "to": "19191234567",
                "data": {
                    "header": ["John"],
                    "body": ["order #1234"],
                },
            }
        ]

    def test_to_json_omits_null_personalization_fields(self, builder):
        """Test that None personalization data fields are omitted from JSON."""
        personalization = WhatsAppPersonalization(
            to="19191234567",
            data=WhatsAppPersonalizationData(body=["Hello"]),
        )

        request = (
            builder.from_number("12345678901")
            .add_recipient("19191234567")
            .template_id("abc123")
            .add_personalization(personalization)
            .build()
        )

        json_data = request.to_json()
        p_data = json_data["personalization"][0]["data"]

        assert "header" not in p_data
        assert "buttons" not in p_data
        assert p_data["body"] == ["Hello"]