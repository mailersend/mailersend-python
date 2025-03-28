import pytest
from pydantic import ValidationError

from mailersend.models.email import (
    EmailRecipient, EmailContent, EmailAttachment, 
    EmailPersonalization, EmailRequest, EmailFrom, EmailReplyTo, EmailTrackingSettings, EmailHeader
)


class TestEmailRecipient:
    def test_valid_recipient(self):
        """Test that valid recipient data passes validation."""
        recipient = EmailRecipient(email="test@example.com", name="John Doe")
        
        assert recipient.email == "test@example.com"
        assert recipient.name == "John Doe"
    
    def test_email_required(self):
        """Test that email is required."""
        with pytest.raises(ValidationError) as exc_info:
            EmailRecipient(name="John Doe")
        
        errors = exc_info.value.errors()
        assert any(error["loc"][0] == "email" and "required" in error["msg"] for error in errors)
    
    def test_name_optional(self):
        """Test that name is optional."""
        recipient = EmailRecipient(email="test@example.com")
        assert recipient.email == "test@example.com"
        assert recipient.name is None
    
    def test_invalid_email(self):
        """Test that invalid email format is rejected."""
        with pytest.raises(ValidationError):
            EmailRecipient(email="not-an-email", name="John Doe")
    
    def test_name_with_semicolon(self):
        """Test that name with semicolon is rejected."""
        with pytest.raises(ValidationError) as exc_info:
            EmailRecipient(email="test@example.com", name="John; Doe")
        
        errors = exc_info.value.errors()
        assert any(";" in error["msg"].lower() for error in errors)
    
    def test_name_with_comma(self):
        """Test that name with comma is rejected."""
        with pytest.raises(ValidationError) as exc_info:
            EmailRecipient(email="test@example.com", name="John, Doe")
        
        errors = exc_info.value.errors()
        assert any("comma" in error["msg"].lower() for error in errors)
    
    def test_to_dict(self):
        """Test conversion to dictionary format."""
        recipient = EmailRecipient(email="test@example.com", name="John Doe")
        recipient_dict = recipient.dict()
        
        assert recipient_dict["email"] == "test@example.com"
        assert recipient_dict["name"] == "John Doe"


class TestEmailContent:
    def test_valid_content(self):
        """Test that valid email content passes validation."""
        content = EmailContent(subject="Test Subject", html="<p>Test HTML</p>")
        
        assert content.subject == "Test Subject"
        assert content.html == "<p>Test HTML</p>"
        assert content.text is None  # Default value
    
    def test_subject_required(self):
        """Test that subject is required."""
        with pytest.raises(ValidationError) as exc_info:
            EmailContent(html="<p>Test HTML</p>")
        
        errors = exc_info.value.errors()
        assert any(error["loc"][0] == "subject" for error in errors)
    
    def test_html_or_text_required(self):
        """Test that either html or text is required."""
        # Both provided - valid
        content = EmailContent(subject="Test", html="<p>HTML</p>", text="Text")
        assert content.html == "<p>HTML</p>"
        assert content.text == "Text"
        
        # Only html provided - valid
        content = EmailContent(subject="Test", html="<p>HTML</p>")
        assert content.html == "<p>HTML</p>"
        assert content.text is None
        
        # Only text provided - valid
        content = EmailContent(subject="Test", text="Text")
        assert content.html is None
        assert content.text == "Text"
        
        # Neither provided - should raise validation error
        with pytest.raises(ValidationError) as exc_info:
            EmailContent(subject="Test")
        
        errors = exc_info.value.errors()
        assert any("least one" in error["msg"].lower() for error in errors)
    
    def test_max_subject_length(self):
        """Test that subject has a maximum length."""
        long_subject = "A" * 1000  # Very long subject
        
        with pytest.raises(ValidationError) as exc_info:
            EmailContent(subject=long_subject, html="<p>Test</p>")
        
        errors = exc_info.value.errors()
        assert any(error["loc"][0] == "subject" and "too long" in error["msg"] for error in errors)


class TestEmailAttachment:
    def test_valid_attachment(self):
        """Test that a valid attachment passes validation."""
        attachment = EmailAttachment(
            content="SGVsbG8gV29ybGQ=",  # Base64 encoded "Hello World"
            filename="test.txt"
        )
        
        assert attachment.content == "SGVsbG8gV29ybGQ="
        assert attachment.filename == "test.txt"
        assert attachment.id is None
        assert attachment.disposition == "attachment"  # Default value
    
    def test_required_fields(self):
        """Test that content and filename are required."""
        # Missing content
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
        """Test that disposition must be one of the allowed values."""
        # Valid - attachment
        attachment = EmailAttachment(
            content="SGVsbG8gV29ybGQ=",
            filename="test.txt",
            disposition="attachment"
        )
        assert attachment.disposition == "attachment"
        
        # Valid - inline
        attachment = EmailAttachment(
            content="SGVsbG8gV29ybGQ=",
            filename="test.txt",
            disposition="inline"
        )
        assert attachment.disposition == "inline"
        
        # Invalid disposition
        with pytest.raises(ValidationError) as exc_info:
            EmailAttachment(
                content="SGVsbG8gV29ybGQ=",
                filename="test.txt",
                disposition="invalid"
            )
        
        errors = exc_info.value.errors()
        assert any(error["loc"][0] == "disposition" for error in errors)
    
    def test_id_optional(self):
        """Test that id is optional."""
        attachment = EmailAttachment(
            content="SGVsbG8gV29ybGQ=",
            filename="test.txt",
            id="test-id"
        )
        assert attachment.id == "test-id"


class TestEmailPersonalization:
    def test_valid_personalization(self):
        """Test that valid personalization passes validation."""
        personalization = EmailPersonalization(
            email="recipient@example.com",
            data={"name": "John", "product": "SDK"}
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
        """Test that data must be a dictionary."""
        with pytest.raises(ValidationError) as exc_info:
            EmailPersonalization(
                email="recipient@example.com",
                data="not-a-dict"
            )
        
        errors = exc_info.value.errors()
        assert any(error["loc"][0] == "data" for error in errors)


class TestEmailRequest:
    def test_valid_request_with_content(self):
        """Test valid email request with direct content."""
        request = EmailRequest(
            from_email=EmailRecipient(email="sender@example.com", name="Sender"),
            to=[EmailRecipient(email="recipient@example.com", name="Recipient")],
            subject="Test Subject",
            html="<p>Test HTML</p>",
            text="Test Text"
        )
        
        assert request.from_email.email == "sender@example.com"
        assert request.to[0].email == "recipient@example.com"
        assert request.subject == "Test Subject"
        assert request.html == "<p>Test HTML</p>"
        assert request.text == "Test Text"
        assert request.template_id is None
    
    def test_valid_request_with_template(self):
        """Test valid email request with template."""
        request = EmailRequest(
            from_email=EmailRecipient(email="sender@example.com", name="Sender"),
            to=[EmailRecipient(email="recipient@example.com", name="Recipient")],
            template_id="template-123"
        )
        
        assert request.from_email.email == "sender@example.com"
        assert request.to[0].email == "recipient@example.com"
        assert request.template_id == "template-123"
        assert request.subject is None
        assert request.html is None
        assert request.text is None
    
    def test_required_fields(self):
        """Test that from_email and to are required."""
        # Missing from_email
        with pytest.raises(ValidationError):
            EmailRequest(
                to=[EmailRecipient(email="recipient@example.com")],
                subject="Test",
                html="<p>Test</p>"
            )
        
        # Missing to
        with pytest.raises(ValidationError):
            EmailRequest(
                from_email=EmailRecipient(email="sender@example.com"),
                subject="Test",
                html="<p>Test</p>"
            )
    
    def test_template_or_content_required(self):
        """Test that either template_id or content is required."""
        # Neither template nor content provided
        with pytest.raises(ValidationError) as exc_info:
            EmailRequest(
                from_email=EmailRecipient(email="sender@example.com"),
                to=[EmailRecipient(email="recipient@example.com")]
            )
        
        errors = exc_info.value.errors()
        assert any("template_id or content" in error["msg"].lower() for error in errors)
    
    def test_cc_and_bcc_optional(self):
        """Test that cc and bcc are optional."""
        request = EmailRequest(
            from_email=EmailRecipient(email="sender@example.com"),
            to=[EmailRecipient(email="recipient@example.com")],
            cc=[EmailRecipient(email="cc@example.com")],
            bcc=[EmailRecipient(email="bcc@example.com")],
            subject="Test",
            html="<p>Test</p>"
        )
        
        assert request.cc[0].email == "cc@example.com"
        assert request.bcc[0].email == "bcc@example.com"
    
    def test_attachments_optional(self):
        """Test that attachments are optional."""
        request = EmailRequest(
            from_email=EmailRecipient(email="sender@example.com"),
            to=[EmailRecipient(email="recipient@example.com")],
            subject="Test",
            html="<p>Test</p>",
            attachments=[
                EmailAttachment(content="SGVsbG8gV29ybGQ=", filename="test.txt")
            ]
        )
        
        assert len(request.attachments) == 1
        assert request.attachments[0].filename == "test.txt"
    
    def test_personalization_optional(self):
        """Test that personalization is optional."""
        request = EmailRequest(
            from_email=EmailRecipient(email="sender@example.com"),
            to=[EmailRecipient(email="recipient@example.com")],
            subject="Test",
            html="<p>Test</p>",
            personalization=[
                EmailPersonalization(
                    email="recipient@example.com",
                    data={"name": "John"}
                )
            ]
        )
        
        assert len(request.personalization) == 1
        assert request.personalization[0].email == "recipient@example.com"
        assert request.personalization[0].data == {"name": "John"}
    
    def test_to_dict_conversion(self):
        """Test conversion to API-compatible dictionary."""
        request = EmailRequest(
            from_email=EmailRecipient(email="sender@example.com", name="Sender"),
            to=[EmailRecipient(email="recipient@example.com", name="Recipient")],
            subject="Test",
            html="<p>Test</p>"
        )
        
        data = request.dict(exclude_none=True)
        
        assert data["from"] == {"email": "sender@example.com", "name": "Sender"}
        assert data["to"] == [{"email": "recipient@example.com", "name": "Recipient"}]
        assert data["subject"] == "Test"
        assert data["html"] == "<p>Test</p>"
        assert "template_id" not in data