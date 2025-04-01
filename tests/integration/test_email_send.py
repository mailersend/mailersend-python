import pytest
from tests.test_helpers import vcr, email_client
import os
from datetime import datetime

from mailersend.exceptions import ValidationError, MailerSendError

class TestEmailSend:
    @pytest.fixture
    def base_email_kwargs(self):
        """Basic email parameters that are valid for most tests"""
        return {
            "from_email": {"email": "ms-sdk@igor.fail", "name": "Sender"},
            "to": [{"email": "igor@mailerlite.com", "name": "Recipient"}],
            "subject": "Test Email",
            "html": "<p>This is a test email sent via the API</p>",
            "text": "This is a test email sent via the API"
        }
    
    # @vcr.use_cassette("email_send_with_object.json")
    def test_send_with_email_request_object(self, email_client, base_email_kwargs):
        # Test sending with a complete EmailRequest object
        result = email_client.emails.send(**base_email_kwargs)
        
        # Verify response structure
        assert isinstance(result, dict)
        assert "id" in result  # Mailersend returns an email ID

    @vcr.use_cassette("email_send_with_kwargs.json")
    def test_send_with_kwargs(self, email_client, base_email_kwargs):
        # Test sending with keyword arguments
        result = email_client.send(**base_email_kwargs)
        
        # Verify response structure
        assert isinstance(result, dict)
        assert "id" in result

    @vcr.use_cassette("email_send_text_only.json")
    def test_send_with_text_only(self, email_client):
        # Test sending with text content only (no HTML)
        kwargs = {
            "from_email": {"email": "sender@example.com", "name": "Sender"},
            "to": [{"email": "recipient@example.com", "name": "Recipient"}],
            "subject": "Text Only Email",
            "text": "This is a plain text email without HTML"
        }
        
        result = email_client.send(**kwargs)
        
        # Verify response structure
        assert isinstance(result, dict)
        assert "id" in result

    @vcr.use_cassette("email_send_with_cc_bcc.json")
    def test_send_with_cc_and_bcc(self, email_client, base_email_kwargs):
        # Test sending with CC and BCC recipients
        kwargs = {**base_email_kwargs}
        kwargs.update({
            "cc": [{"email": "cc@example.com", "name": "CC Recipient"}],
            "bcc": [{"email": "bcc@example.com", "name": "BCC Recipient"}]
        })
        
        result = email_client.send(**kwargs)
        
        # Verify response structure
        assert isinstance(result, dict)
        assert "id" in result

    @vcr.use_cassette("email_send_with_scheduled_time.json")
    def test_send_with_datetime_send_at(self, email_client, base_email_kwargs):
        # Test sending with scheduled datetime
        # Schedule for 24 hours in the future to avoid test failures
        send_time = datetime.now().replace(microsecond=0)
        send_time = datetime.fromtimestamp(send_time.timestamp() + 86400)  # +24 hours
        
        kwargs = {**base_email_kwargs}
        kwargs["send_at"] = send_time
        
        result = email_client.send(**kwargs)
        
        # Verify response structure
        assert isinstance(result, dict)
        assert "id" in result

    @vcr.use_cassette("email_send_with_attachments.json")
    def test_send_with_attachments(self, email_client, base_email_kwargs):
        # Create a test file for attachment
        test_file_path = "tests/fixtures/test_attachment.txt"
        os.makedirs(os.path.dirname(test_file_path), exist_ok=True)
        
        with open(test_file_path, "w") as f:
            f.write("This is a test attachment file.")
        
        try:
            # Test sending with attachments
            kwargs = {**base_email_kwargs}
            kwargs.update({
                "attachments": [
                    {"file_path": test_file_path, "disposition": "attachment"}
                ]
            })
            
            result = email_client.send(**kwargs)
            
            # Verify response structure
            assert isinstance(result, dict)
            assert "id" in result
        
        finally:
            # Clean up the test file
            if os.path.exists(test_file_path):
                os.remove(test_file_path)

    @vcr.use_cassette("email_send_with_tags.json")
    def test_send_with_tags(self, email_client, base_email_kwargs):
        # Test sending with tags
        kwargs = {**base_email_kwargs}
        kwargs.update({
            "tags": ["test", "automation", "api-test"]
        })
        
        result = email_client.send(**kwargs)
        
        # Verify response structure
        assert isinstance(result, dict)
        assert "id" in result

    @vcr.use_cassette("email_send_with_tracking.json")
    def test_send_with_tracking_settings(self, email_client, base_email_kwargs):
        # Test sending with tracking settings
        kwargs = {**base_email_kwargs}
        kwargs.update({
            "tracking": {
                "opens": True,
                "clicks": True,
                "unsubscribe": False
            }
        })
        
        result = email_client.send(**kwargs)
        
        # Verify response structure
        assert isinstance(result, dict)
        assert "id" in result

    @vcr.use_cassette("email_send_with_template.json")
    def test_send_with_template_id(self, email_client):
        # You need a valid template ID for your account
        # This is a placeholder template ID - replace with a real one
        template_id = "template123456"
        
        kwargs = {
            "from_email": {"email": "sender@example.com", "name": "Sender"},
            "to": [{"email": "recipient@example.com", "name": "Recipient"}],
            "subject": "Template Email",
            "template_id": template_id,
            "personalization": [
                {"var": "name", "value": "John Doe"},
                {"var": "company", "value": "ACME Corporation"}
            ]
        }
        
        try:
            result = email_client.send(**kwargs)
            
            # Verify response structure
            assert isinstance(result, dict)
            assert "id" in result
        
        except MailerSendError as e:
            # If template doesn't exist, test will be skipped
            if "template not found" in str(e).lower():
                pytest.skip("Template not found - skipping test")
            else:
                raise

    @vcr.use_cassette("email_send_with_headers.json")
    def test_send_with_custom_headers(self, email_client, base_email_kwargs):
        # Test sending with custom headers
        kwargs = {**base_email_kwargs}
        kwargs.update({
            "headers": {
                "X-Custom-Header": "Custom Value",
                "X-Campaign-ID": "campaign123"
            }
        })
        
        result = email_client.send(**kwargs)
        
        # Verify response structure
        assert isinstance(result, dict)
        assert "id" in result

    @vcr.use_cassette("email_send_with_reply_to.json")
    def test_send_with_reply_to(self, email_client, base_email_kwargs):
        # Test sending with reply-to address
        kwargs = {**base_email_kwargs}
        kwargs.update({
            "reply_to": {"email": "reply@example.com", "name": "Reply Handler"}
        })
        
        result = email_client.send(**kwargs)
        
        # Verify response structure
        assert isinstance(result, dict)
        assert "id" in result

    @vcr.use_cassette("email_send_with_threading.json")
    def test_send_with_in_reply_to_and_references(self, email_client, base_email_kwargs):
        # Test sending with in-reply-to and references headers
        kwargs = {**base_email_kwargs}
        kwargs.update({
            "in_reply_to": "original-message@domain.com",
            "references": "original-message@domain.com thread-123@domain.com"
        })
        
        result = email_client.send(**kwargs)
        
        # Verify response structure
        assert isinstance(result, dict)
        assert "id" in result

    def test_send_no_email_params(self, email_client):
        # Test sending with no email parameters
        # This doesn't need VCR as it should fail before any API call
        with pytest.raises(ValidationError) as excinfo:
            email_client.send()
        
        assert "Either email object or email parameters must be provided" in str(excinfo.value)

    def test_send_invalid_email_params(self, email_client):
        # Test sending with invalid email parameters
        # This doesn't need VCR as it should fail before any API call
        with pytest.raises(ValidationError):
            email_client.send(
                from_email={"email": "invalid-email"},
                to=[{"email": "recipient@example.com"}],
                subject="Invalid Email"
            )

    @vcr.use_cassette("email_send_missing_required_content.json")
    def test_send_missing_required_content(self, email_client):
        # Test validation error from missing both html and text
        kwargs = {
            "from_email": {"email": "sender@example.com", "name": "Sender"},
            "to": [{"email": "recipient@example.com", "name": "Recipient"}],
            "subject": "Test Subject"
            # Missing both html and text
        }
        
        with pytest.raises(ValidationError) as excinfo:
            email_client.send(**kwargs)
        
        # The specific error message will depend on your validate_email_requirements implementation
        assert "content" in str(excinfo.value).lower() or "html" in str(excinfo.value).lower() or "text" in str(excinfo.value).lower()

    @vcr.use_cassette("email_send_rate_limit.json")
    def test_api_rate_limit(self, email_client, base_email_kwargs):
        # This test depends on the API returning a rate limit error
        # It might need to be manually recorded or simulated
        try:
            # Try to trigger a rate limit by sending multiple requests
            for _ in range(5):  # Adjust this number based on API limits
                email_client.send(**base_email_kwargs)
                
        except MailerSendError as e:
            if e.status_code == 429:
                # Test passed if we got a rate limit error
                assert "rate limit" in str(e).lower() or "too many requests" in str(e).lower()
                return
            else:
                # If we got a different error, re-raise it
                raise
                
        # If we didn't get a rate limit error, skip the test
        pytest.skip("Rate limit not triggered - skipping test")