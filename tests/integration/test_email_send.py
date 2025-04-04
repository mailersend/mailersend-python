import pytest
from tests.test_helpers import vcr, email_client
import os
import copy
import base64
from datetime import datetime

from mailersend.exceptions import ValidationError, MailerSendError
from mailersend.models.email import (
    EmailContact, EmailAttachment,
    EmailPersonalization, EmailRequest,
    EmailTrackingSettings, EmailHeader
)

@pytest.fixture
def base_email_request():
    """Basic email parameters that are valid for most tests"""
    return EmailRequest(
        from_email=EmailContact(email=os.environ.get("SDK_FROM_EMAIL"), name="Sender"),
        to=[EmailContact(email=os.environ.get("SDK_TO_EMAIL"), name="Recipient")],
        subject="Test Email",
        html="<p>This is a test email</p>"
    )

@pytest.fixture
def email_request_factory():
    def _factory(base: EmailRequest, **overrides) -> EmailRequest:
        # Create a new EmailRequest with the same fields, overridden with kwargs
        data = base.model_dump()

        # Remove fields explicitly set to `None` in overrides
        for key, value in overrides.items():
            if value is None:
                data.pop(key, None)
            else:
                data[key] = value

        return EmailRequest(**data)

    return _factory

class TestEmailSend:   
    @vcr.use_cassette("email_send_with_base_params.json")
    def test_send_with_email_request_object(self, email_client, base_email_request, email_request_factory):
        # Test sending with a complete EmailRequest object
        email_request = email_request_factory(
            base_email_request,
            html="<p>This is a test email</p>"
        )

        result = email_client.emails.send(email_request)
        
        # Verify response structure
        assert isinstance(result, dict)
        assert "id" in result


    @vcr.use_cassette("email_send_text_only.json")
    def test_send_with_text_only(self, email_client, base_email_request, email_request_factory):
        # Test sending with text content only (no HTML)
        email_request = email_request_factory(
            base_email_request,
            html=None,
            text="This is a test email"
        )

        result = email_client.emails.send(email_request)
        
        # Verify response structure
        assert isinstance(result, dict)
        assert "id" in result

    @vcr.use_cassette("email_send_with_cc_bcc.json")
    def test_send_with_cc_and_bcc(self, email_client, base_email_request, email_request_factory):
        # Test sending with CC and BCC recipients
        email_request = email_request_factory(
            base_email_request,
            cc=[
                EmailContact(email=os.environ.get("SDK_CC_EMAIL"), name="Recipient")
            ],
            bcc = [
                EmailContact(email=os.environ.get("SDK_BCC_EMAIL"), name="Recipient")
            ]
        )

        result = email_client.emails.send(email_request)
        
        # Verify response structure
        assert isinstance(result, dict)
        assert "id" in result

    @vcr.use_cassette("email_send_with_scheduled_time.json")
    def test_send_with_datetime_send_at(self, email_client, base_email_request, email_request_factory):
        # Test sending with scheduled datetime
        # Schedule for 24 hours in the future to avoid test failures
        send_time = datetime.now().replace(microsecond=0)
        send_time = datetime.fromtimestamp(send_time.timestamp() + 86400)  # +24 hours

        email_request = email_request_factory(
            base_email_request,
            send_at = int(send_time.timestamp())
        )

        result = email_client.emails.send(email_request)
        
        # Verify response structure
        assert isinstance(result, dict)
        assert "id" in result

    @vcr.use_cassette("email_send_with_attachments.json")
    def test_send_with_attachments(self, email_client, base_email_request, email_request_factory):
        # Create a test file for attachment
        test_file_path = "tests/fixtures/test_attachment.txt"
        os.makedirs(os.path.dirname(test_file_path), exist_ok=True)
        
        with open(test_file_path, "w") as f:
            f.write("This is a test attachment file.")

        # Read the file and base64-encode its content
        with open(test_file_path, "rb") as f:
            encoded_content = base64.b64encode(f.read()).decode()

        attachment = EmailAttachment(
            content=encoded_content,
            disposition="attachment",
            filename="test_attachment.txt",
        )
        
        try:
            # Test sending with attachments
            email_request = email_request_factory(
                base_email_request,
                attachments = [attachment]
            )
            
            result = email_client.emails.send(email_request)
            
            # Verify response structure
            assert isinstance(result, dict)
            assert "id" in result
        
        finally:
            # Clean up the test file
            if os.path.exists(test_file_path):
                os.remove(test_file_path)

    @vcr.use_cassette("email_send_with_tags.json")
    def test_send_with_tags(self, email_client, base_email_request, email_request_factory):
        # Test sending with tags
        email_request = email_request_factory(
            base_email_request,
            tags=["test", "automation", "api-test"]
        )
        
        result = email_client.emails.send(email_request)
        
        # Verify response structure
        assert isinstance(result, dict)
        assert "id" in result

    @vcr.use_cassette("email_send_with_tracking.json")
    def test_send_with_tracking_settings(self, email_client, base_email_request, email_request_factory):
        # Test sending with tracking settings
        email_request = email_request_factory(
            base_email_request,
            settings=EmailTrackingSettings(track_clicks=True, track_opens=True, track_content=False)
        )

        result = email_client.emails.send(email_request)
        
        # Verify response structure
        assert isinstance(result, dict)
        assert "id" in result

    @vcr.use_cassette("email_send_with_template.json")
    def test_send_with_template_id(self, email_client, base_email_request, email_request_factory):
        # Send email using template ID
        email_request = email_request_factory(
            base_email_request,
            template_id=os.environ.get("SDK_TEMPLATE_ID"),
            personalization=[
                    EmailPersonalization(
                    email=os.environ.get("SDK_TO_EMAIL"),
                    data={"name": "Recipient Name"}
                )
            ]
        )
        
        result = email_client.emails.send(email_request)

        # Verify response structure
        assert isinstance(result, dict)
        assert "id" in result

    @vcr.use_cassette("email_send_with_headers.json")
    def test_send_with_custom_headers(self, email_client, base_email_request, email_request_factory):
        # Test sending with custom headers
        email_request = email_request_factory(
            base_email_request,
            headers=[
                EmailHeader(name="X-Custom-Header", value="Custom Value"),
            ]
        )
        
        result = email_client.emails.send(email_request)
        
        # Verify response structure
        assert isinstance(result, dict)
        assert "id" in result

    @vcr.use_cassette("email_send_with_reply_to.json")
    def test_send_with_reply_to(self, email_client, base_email_request, email_request_factory):
        # Test sending with reply-to address
        email_request = email_request_factory(
            base_email_request,
            reply_to=EmailContact(email=os.environ.get("SDK_REPLY_TO_EMAIL"), name="Reply Handler")
        )
        
        result = email_client.emails.send(email_request)
        
        # Verify response structure
        assert isinstance(result, dict)
        assert "id" in result

    @vcr.use_cassette("email_send_with_threading.json")
    def test_send_with_in_reply_to_and_references(self, email_client, base_email_request, email_request_factory):
        # Test sending with in-reply-to and references headers
        email_request = email_request_factory(
            base_email_request,
            in_reply_to=os.environ.get("SDK_REPLY_TO_EMAIL"),
            references=["123456"]
        )
        
        result = email_client.emails.send(email_request)
        
        # Verify response structure
        assert isinstance(result, dict)
        assert "id" in result