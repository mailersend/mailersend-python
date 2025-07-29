import pytest
from pydantic import ValidationError

from mailersend.models.email import (
    EmailContact,
    EmailAttachment,
    EmailPersonalization,
    EmailRequest,
    EmailTrackingSettings,
    EmailHeader,
)


class TestEmailContact:
    def test_valid_recipient(self):
        recipient = EmailContact(email="test@example.com", name="John Doe")

        assert recipient.email == "test@example.com"
        assert recipient.name == "John Doe"

    def test_email_required(self):
        with pytest.raises(ValidationError) as exc_info:
            EmailContact(name="John Doe")

        errors = exc_info.value.errors()
        assert any(
            error["loc"][0] == "email" and "required" in error["msg"]
            for error in errors
        )

    def test_name_optional(self):
        recipient = EmailContact(email="test@example.com")
        assert recipient.email == "test@example.com"
        assert recipient.name is None

    def test_invalid_email(self):
        with pytest.raises(ValidationError):
            EmailContact(email="not-an-email", name="John Doe")

    def test_to_dict(self):
        recipient = EmailContact(email="test@example.com", name="John Doe")
        recipient_dict = recipient.model_dump()

        assert recipient_dict["email"] == "test@example.com"
        assert recipient_dict["name"] == "John Doe"


class TestEmailAttachment:
    def test_valid_attachment(self):
        attachment = EmailAttachment(
            content="SGVsbG8gV29ybGQ=",  # Base64 encoded "Hello World"
            filename="test.txt",
            disposition="attachment",
        )

        assert attachment.content == "SGVsbG8gV29ybGQ="
        assert attachment.filename == "test.txt"
        assert attachment.id is None
        assert attachment.disposition == "attachment"  # Default value

    def test_required_fields(self):
        with pytest.raises(ValidationError) as exc_info:
            EmailAttachment(filename="test.txt")

        errors = exc_info.value.errors()
        assert any(error["loc"][0] == "content" for error in errors)

        # Missing filename
        with pytest.raises(ValidationError) as exc_info:
            EmailAttachment(content="SGVsbG8gV29ybGQ=")

        errors = exc_info.value.errors()
        assert any(error["loc"][0] == "filename" for error in errors)

    def test_disposition_validation(self):
        # Valid - attachment
        attachment = EmailAttachment(
            content="SGVsbG8gV29ybGQ=", filename="test.txt", disposition="attachment"
        )
        assert attachment.disposition == "attachment"

        # Valid - inline
        attachment = EmailAttachment(
            content="SGVsbG8gV29ybGQ=", filename="test.txt", disposition="inline"
        )
        assert attachment.disposition == "inline"

        # Invalid disposition
        with pytest.raises(ValidationError) as exc_info:
            EmailAttachment(
                content="SGVsbG8gV29ybGQ=", filename="test.txt", disposition="invalid"
            )

        errors = exc_info.value.errors()
        assert any(error["loc"][0] == "disposition" for error in errors)

    def test_id_optional(self):
        """Test that id is optional."""
        attachment = EmailAttachment(
            content="SGVsbG8gV29ybGQ=",
            filename="test.txt",
            disposition="attachment",
            id="test-id",
        )
        assert attachment.id == "test-id"


class TestEmailPersonalization:
    def test_valid_personalization(self):
        personalization = EmailPersonalization(
            email="recipient@example.com", data={"name": "John", "product": "SDK"}
        )

        assert personalization.email == "recipient@example.com"
        assert personalization.data == {"name": "John", "product": "SDK"}

    def test_email_required(self):
        """Test that email is required."""
        with pytest.raises(ValidationError) as exc_info:
            EmailPersonalization(data={"name": "John"})

        errors = exc_info.value.errors()
        assert any(error["loc"][0] == "email" for error in errors)

    def test_data_required(self):
        """Test that data is required."""
        with pytest.raises(ValidationError) as exc_info:
            EmailPersonalization(email="recipient@example.com")

        errors = exc_info.value.errors()
        assert any(error["loc"][0] == "data" for error in errors)

    def test_data_must_be_dict(self):
        with pytest.raises(ValidationError) as exc_info:
            EmailPersonalization(email="recipient@example.com", data="not-a-dict")

        errors = exc_info.value.errors()
        assert any(error["loc"][0] == "data" for error in errors)


class TestEmailRequest:
    def test_valid_request_with_content(self):
        request = EmailRequest(
            from_email=EmailContact(email="sender@example.com", name="Sender"),
            to=[EmailContact(email="recipient@example.com", name="Recipient")],
            subject="Test Subject",
            html="<p>Test HTML</p>",
            text="Test Text",
        )

        assert request.from_email.email == "sender@example.com"
        assert request.to[0].email == "recipient@example.com"
        assert request.subject == "Test Subject"
        assert request.html == "<p>Test HTML</p>"
        assert request.text == "Test Text"
        assert request.template_id is None

    def test_valid_request_with_template(self):
        request = EmailRequest(
            from_email=EmailContact(email="sender@example.com", name="Sender"),
            to=[EmailContact(email="recipient@example.com", name="Recipient")],
            subject="Test Subject",
            template_id="template-123",
        )

        assert request.from_email.email == "sender@example.com"
        assert request.to[0].email == "recipient@example.com"
        assert request.template_id == "template-123"
        assert request.subject is "Test Subject"
        assert request.html is None
        assert request.text is None

    def test_required_fields(self):
        # Missing from_email
        with pytest.raises(ValidationError):
            EmailRequest(
                to=[EmailContact(email="recipient@example.com")],
                subject="Test",
                html="<p>Test</p>",
            )

        # Missing to
        with pytest.raises(ValidationError):
            EmailRequest(
                from_email=EmailContact(email="sender@example.com"),
                subject="Test",
                html="<p>Test</p>",
            )

    def test_cc_and_bcc_optional(self):
        request = EmailRequest(
            from_email=EmailContact(email="sender@example.com"),
            to=[EmailContact(email="recipient@example.com")],
            cc=[EmailContact(email="cc@example.com")],
            bcc=[EmailContact(email="bcc@example.com")],
            subject="Test",
            html="<p>Test</p>",
        )

        assert request.cc[0].email == "cc@example.com"
        assert request.bcc[0].email == "bcc@example.com"

    def test_attachments_optional(self):
        request = EmailRequest(
            from_email=EmailContact(email="sender@example.com"),
            to=[EmailContact(email="recipient@example.com")],
            subject="Test",
            html="<p>Test</p>",
            attachments=[
                EmailAttachment(
                    content="SGVsbG8gV29ybGQ=",
                    filename="test.txt",
                    disposition="inline",
                )
            ],
        )

        assert len(request.attachments) == 1
        assert request.attachments[0].filename == "test.txt"

    def test_personalization_optional(self):
        request = EmailRequest(
            from_email=EmailContact(email="sender@example.com"),
            to=[EmailContact(email="recipient@example.com")],
            subject="Test",
            html="<p>Test</p>",
            personalization=[
                EmailPersonalization(
                    email="recipient@example.com", data={"name": "John"}
                )
            ],
        )

        assert len(request.personalization) == 1
        assert request.personalization[0].email == "recipient@example.com"
        assert request.personalization[0].data == {"name": "John"}

    def test_tags_within_limit(self):
        # Test with no tags
        request = EmailRequest(
            from_email=EmailContact(email="sender@example.com"),
            to=[EmailContact(email="recipient@example.com")],
            subject="Test",
            html="<p>Test</p>",
        )
        assert request.tags is None

        # Test with empty list
        request = EmailRequest(
            from_email=EmailContact(email="sender@example.com"),
            to=[EmailContact(email="recipient@example.com")],
            subject="Test",
            html="<p>Test</p>",
            tags=[],
        )
        assert request.tags == []

        # Test with 1 tag
        request = EmailRequest(
            from_email=EmailContact(email="sender@example.com"),
            to=[EmailContact(email="recipient@example.com")],
            subject="Test",
            html="<p>Test</p>",
            tags=["tag1"],
        )
        assert request.tags == ["tag1"]

        # Test with 5 tags (max allowed)
        request = EmailRequest(
            from_email=EmailContact(email="sender@example.com"),
            to=[EmailContact(email="recipient@example.com")],
            subject="Test",
            html="<p>Test</p>",
            tags=["tag1", "tag2", "tag3", "tag4", "tag5"],
        )

        assert len(request.tags) == 5

    def test_tags_exceed_limit(self):
        # Test with 6 tags (exceeds limit)
        with pytest.raises(ValidationError) as exc_info:
            request = EmailRequest(
                from_email=EmailContact(email="sender@example.com"),
                to=[EmailContact(email="recipient@example.com")],
                subject="Test",
                html="<p>Test</p>",
                tags=["tag1", "tag2", "tag3", "tag4", "tag5", "tag6"],
            )

        errors = exc_info.value.errors()
        assert any(
            "Maximum 5 tags are allowed" in str(error["msg"]) for error in errors
        )

    # Tests for to validator
    def test_to_within_limit(self):
        # Test with 1 recipient (min allowed)
        request = EmailRequest(
            from_email=EmailContact(email="sender@example.com"),
            to=[EmailContact(email="recipient@example.com")],
            subject="Test",
            html="<p>Test</p>",
        )
        assert len(request.to) == 1

        # Test with 51 recipients
        recipients = [
            EmailContact(email=f"recipient{i}@example.com") for i in range(1, 52)
        ]
        with pytest.raises(ValidationError) as exc_info:
            request = EmailRequest(
                from_email=EmailContact(email="sender@example.com"),
                to=recipients,
                subject="Test",
                html="<p>Test</p>",
            )

        errors = exc_info.value.errors()
        assert any(
            "'to' must contain between 1 and 50 recipients" in str(error["msg"])
            for error in errors
        )

    def test_to_dict_conversion(self):
        """Test conversion to API-compatible dictionary."""
        request = EmailRequest(
            from_email=EmailContact(email="sender@example.com", name="Sender"),
            to=[EmailContact(email="recipient@example.com", name="Recipient")],
            subject="Test",
            html="<p>Test</p>",
        )

        data = request.model_dump(exclude_none=True)

        assert data["from_email"] == {"email": "sender@example.com", "name": "Sender"}
        assert data["to"] == [{"email": "recipient@example.com", "name": "Recipient"}]
        assert data["subject"] == "Test"
        assert data["html"] == "<p>Test</p>"
        assert "template_id" not in data
