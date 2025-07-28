import pytest
from tests.test_helpers import vcr, email_client
import os
import base64
from datetime import datetime

from mailersend.models.email import (
    EmailContact, EmailAttachment,
    EmailPersonalization, EmailRequest,
    EmailTrackingSettings, EmailHeader
)
from mailersend.models.base import APIResponse

@pytest.fixture
def base_email_request():
    """Basic email parameters that are valid for most tests"""
    return EmailRequest(
        from_email=EmailContact(email=os.environ.get("SDK_FROM_EMAIL"), name="Sender"),
        to=[EmailContact(email=os.environ.get("SDK_TO_EMAIL"), name="Recipient")],
        subject="Test Email",
        html="<p>This is a test email</p>"
    )

def email_request_factory(base: EmailRequest, **overrides) -> EmailRequest:
    """Create a new EmailRequest with the same fields, overridden with kwargs"""
    data = base.model_dump()

    # Remove fields explicitly set to `None` in overrides
    for key, value in overrides.items():
        if value is None:
            data.pop(key, None)
        else:
            data[key] = value

    return EmailRequest(**data)


@pytest.fixture(autouse=True)
def inject_common_objects(request, email_client, base_email_request):
    if hasattr(request, "cls") and request.cls is not None:
        request.cls.email_client = email_client
        request.cls.base_email_request = base_email_request
        request.cls.email_request_factory = staticmethod(email_request_factory)

class TestEmailSend:   
    @vcr.use_cassette("email_send_with_base_params.yaml")
    def test_send_with_email_request_object(self):
        # Test sending with a complete EmailRequest object
        email_request = self.email_request_factory(
            self.base_email_request,
            html="<p>This is a test email</p>"
        )

        result = self.email_client.emails.send(email_request)
        
        assert isinstance(result, APIResponse)
        assert result.success is True
        assert "id" in result
        assert result["id"] is not None
        assert result.status_code == 202
        assert isinstance(result.headers, dict)


    @vcr.use_cassette("email_send_text_only.yaml")
    def test_send_with_text_only(self):
        # Test sending with text content only (no HTML)
        email_request = self.email_request_factory(
            self.base_email_request,
            html=None,
            text="This is a test email"
        )

        result = self.email_client.emails.send(email_request)
        
        # Verify response structure
        assert isinstance(result, APIResponse)
        assert result.success is True
        assert "id" in result
        assert result["id"] is not None

    @vcr.use_cassette("email_send_with_cc_bcc.yaml")
    def test_send_with_cc_and_bcc(self):
        # Test sending with CC and BCC recipients
        email_request = self.email_request_factory(
            self.base_email_request,
            cc=[
                EmailContact(email=os.environ.get("SDK_CC_EMAIL"), name="Recipient")
            ],
            bcc = [
                EmailContact(email=os.environ.get("SDK_BCC_EMAIL"), name="Recipient")
            ]
        )

        result = self.email_client.emails.send(email_request)
        
        # Verify response structure
        assert isinstance(result, APIResponse)
        assert result.success is True
        assert "id" in result
        assert result["id"] is not None

    @vcr.use_cassette("email_send_with_scheduled_time.yaml")
    def test_send_with_datetime_send_at(self):
        # Test sending with scheduled datetime
        # Schedule for 24 hours in the future to avoid test failures
        send_time = datetime.now().replace(microsecond=0)
        send_time = datetime.fromtimestamp(send_time.timestamp() + 86400)  # +24 hours

        email_request = self.email_request_factory(
            self.base_email_request,
            send_at = int(send_time.timestamp())
        )

        result = self.email_client.emails.send(email_request)
        
        # Verify response structure
        assert isinstance(result, APIResponse)
        assert result.success is True
        assert "id" in result
        assert result["id"] is not None

    @vcr.use_cassette("email_send_with_attachments.yaml")
    def test_send_with_attachments(self):
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
            email_request = self.email_request_factory(
                self.base_email_request,
                attachments = [attachment]
            )
            
            result = self.email_client.emails.send(email_request)
            
            # Verify response structure
            assert isinstance(result, APIResponse)
            assert result.success is True
            assert "id" in result
            assert result["id"] is not None
        
        finally:
            # Clean up the test file
            if os.path.exists(test_file_path):
                os.remove(test_file_path)

    @vcr.use_cassette("email_send_with_tags.yaml")
    def test_send_with_tags(self):
        # Test sending with tags
        email_request = self.email_request_factory(
            self.base_email_request,
            tags=["test", "automation", "api-test"]
        )
        
        result = self.email_client.emails.send(email_request)
        
        # Verify response structure
        assert isinstance(result, APIResponse)
        assert result.success is True
        assert "id" in result
        assert result["id"] is not None

    @vcr.use_cassette("email_send_with_tracking.yaml")
    def test_send_with_tracking_settings(self):
        # Test sending with tracking settings
        email_request = self.email_request_factory(
            self.base_email_request,
            settings=EmailTrackingSettings(track_clicks=True, track_opens=True, track_content=False)
        )

        result = self.email_client.emails.send(email_request)
        
        # Verify response structure
        assert isinstance(result, APIResponse)
        assert result.success is True
        assert "id" in result
        assert result["id"] is not None

    @vcr.use_cassette("email_send_with_template.yaml")
    def test_send_with_template_id(self):
        # Send email using template ID
        email_request = self.email_request_factory(
            self.base_email_request,
            template_id=os.environ.get("SDK_TEMPLATE_ID"),
            personalization=[
                    EmailPersonalization(
                    email=os.environ.get("SDK_TO_EMAIL"),
                    data={"name": "Recipient Name"}
                )
            ]
        )
        
        result = self.email_client.emails.send(email_request)

        # Verify response structure
        assert isinstance(result, APIResponse)
        assert result.success is True
        assert "id" in result
        assert result["id"] is not None

    @vcr.use_cassette("email_send_with_headers.yaml")
    def test_send_with_custom_headers(self):
        # Test sending with custom headers
        email_request = self.email_request_factory(
            self.base_email_request,
            headers=[
                EmailHeader(name="X-Custom-Header", value="Custom Value"),
            ]
        )
        
        result = self.email_client.emails.send(email_request)
        
        # Verify response structure
        assert isinstance(result, APIResponse)
        assert result.success is True
        assert "id" in result
        assert result["id"] is not None

    @vcr.use_cassette("email_send_with_reply_to.yaml")
    def test_send_with_reply_to(self):
        # Test sending with reply-to address
        email_request = self.email_request_factory(
            self.base_email_request,
            reply_to=EmailContact(email=os.environ.get("SDK_REPLY_TO_EMAIL"), name="Reply Handler")
        )
        
        result = self.email_client.emails.send(email_request)
        
        # Verify response structure
        assert isinstance(result, APIResponse)
        assert result.success is True
        assert "id" in result
        assert result["id"] is not None

    @vcr.use_cassette("email_send_with_threading.yaml")
    def test_send_with_in_reply_to_and_references(self):
        # Test sending with in-reply-to and references headers
        email_request = self.email_request_factory(
            self.base_email_request,
            in_reply_to=os.environ.get("SDK_REPLY_TO_EMAIL"),
            references=["123456"]
        )
        
        result = self.email_client.emails.send(email_request)
        
        # Verify response structure
        assert isinstance(result, APIResponse)
        assert result.success is True
        assert "id" in result
        assert result["id"] is not None

    @vcr.use_cassette("email_send_bulk.yaml")
    def test_send_bulk_emails(self):
        # Test sending bulk emails with multiple EmailRequests
        payload = [
            self.email_request_factory(
                self.base_email_request,
                html="<p>First Email</p>"
            ),
            self.email_request_factory(
                self.base_email_request,
                html="<p>Second Email</p>"
            ),
        ]

        result = self.email_client.emails.send_bulk(payload)

        # Verify response structure
        assert isinstance(result, APIResponse)
        assert result.success is True
        assert "bulk_email_id" in result
        assert result["bulk_email_id"] is not None
        assert result.status_code == 202

    @vcr.use_cassette("email_send_bulk_status.yaml")
    def test_get_bulk_status(self):
        # Test getting the status of a bulk email send
        bulk_email_id = os.environ.get("SDK_BULK_EMAIL_ID")
        
        result = self.email_client.emails.get_bulk_status(bulk_email_id)

        # Verify response structure
        assert isinstance(result, APIResponse)
        assert result.success is True
        # The bulk status response has a "data" wrapper
        assert "data" in result
        assert "id" in result["data"]
        assert "messages_id" in result["data"]
        assert result.status_code == 200
        assert isinstance(result.headers, dict)

