"""Unit tests for WhatsApp models."""

import pytest
from pydantic import ValidationError

from mailersend.models.whatsapp import (
    WhatsAppPersonalization,
    WhatsAppPersonalizationData,
    WhatsAppSendRequest,
)


class TestWhatsAppPersonalizationData:
    """Test WhatsAppPersonalizationData model."""

    def test_all_sections_optional(self):
        """Test that every section may be omitted."""
        data = WhatsAppPersonalizationData()

        assert data.header is None
        assert data.body is None
        assert data.buttons is None

    @pytest.mark.parametrize(
        "section,limit",
        [("header", 60), ("body", 1024), ("buttons", 2000)],
    )
    def test_value_at_limit_is_accepted(self, section, limit):
        """Test a value exactly at the section's character limit."""
        data = WhatsAppPersonalizationData(**{section: ["a" * limit]})

        assert getattr(data, section) == ["a" * limit]

    @pytest.mark.parametrize(
        "section,limit",
        [("header", 60), ("body", 1024), ("buttons", 2000)],
    )
    def test_value_over_limit_is_rejected(self, section, limit):
        """Test a value one character over the section's limit."""
        with pytest.raises(
            ValueError, match=f"Each {section} value must be at most {limit} characters"
        ):
            WhatsAppPersonalizationData(**{section: ["a" * (limit + 1)]})

    def test_limit_applies_to_every_value(self):
        """Test that a later oversized value is caught, not just the first."""
        with pytest.raises(ValueError, match="Each body value must be at most 1024"):
            WhatsAppPersonalizationData(body=["fine", "a" * 1025])

    def test_sections_have_independent_limits(self):
        """Test that a value valid for body is rejected for header."""
        assert WhatsAppPersonalizationData(body=["a" * 100]).body == ["a" * 100]

        with pytest.raises(ValueError, match="Each header value must be at most 60"):
            WhatsAppPersonalizationData(header=["a" * 100])


class TestWhatsAppSendRequest:
    """Test WhatsAppSendRequest model."""

    def test_sender_id_accepted_as_from(self):
        """Test that a MailerSend sender ID is a valid sender identifier."""
        request = WhatsAppSendRequest(
            from_number="3enl6x27wmrxrl2v",
            to=["+48600000001"],
            template_id="23zxk54v6gjy6v7m",
        )

        assert request.from_number == "3enl6x27wmrxrl2v"

    def test_bsuid_accepted_as_recipient(self):
        """Test that a BSUID is a valid recipient."""
        request = WhatsAppSendRequest(
            from_number="15550001234",
            to=["US.13491208655302741918"],
            template_id="23zxk54v6gjy6v7m",
        )

        assert request.to == ["US.13491208655302741918"]

    def test_recipients_at_limit_accepted(self):
        """Test the documented maximum of 10 recipients."""
        recipients = [f"+4860000000{i}" for i in range(10)]
        request = WhatsAppSendRequest(
            from_number="15550001234", to=recipients, template_id="abc123"
        )

        assert len(request.to) == 10

    def test_recipients_over_limit_rejected(self):
        """Test that an 11th recipient is rejected."""
        recipients = [f"+486000000{i:02d}" for i in range(11)]

        with pytest.raises(ValidationError):
            WhatsAppSendRequest(
                from_number="15550001234", to=recipients, template_id="abc123"
            )

    def test_personalization_at_limit_accepted(self):
        """Test the documented maximum of 10 personalization entries."""
        recipients = [f"+4860000000{i}" for i in range(10)]
        personalization = [
            WhatsAppPersonalization(
                to=recipient, data=WhatsAppPersonalizationData(body=["John"])
            )
            for recipient in recipients
        ]

        request = WhatsAppSendRequest(
            from_number="15550001234",
            to=recipients,
            template_id="abc123",
            personalization=personalization,
        )

        assert len(request.personalization) == 10

    def test_personalization_over_limit_rejected(self):
        """Test that an 11th personalization entry is rejected."""
        recipients = [f"+4860000000{i}" for i in range(10)]
        personalization = [
            WhatsAppPersonalization(
                to=recipients[0], data=WhatsAppPersonalizationData(body=["John"])
            )
            for _ in range(11)
        ]

        with pytest.raises(ValidationError):
            WhatsAppSendRequest(
                from_number="15550001234",
                to=recipients,
                template_id="abc123",
                personalization=personalization,
            )

    def test_personalization_recipient_must_be_in_to(self):
        """Test personalization targeting an unlisted recipient."""
        with pytest.raises(ValueError, match="Personalization recipients not in"):
            WhatsAppSendRequest(
                from_number="15550001234",
                to=["+48600000001"],
                template_id="abc123",
                personalization=[
                    WhatsAppPersonalization(
                        to="+48600000002",
                        data=WhatsAppPersonalizationData(body=["John"]),
                    )
                ],
            )

    def test_empty_recipient_rejected(self):
        """Test that a blank recipient is rejected."""
        with pytest.raises(ValueError, match="All recipients must be non-empty"):
            WhatsAppSendRequest(
                from_number="15550001234", to=["   "], template_id="abc123"
            )
