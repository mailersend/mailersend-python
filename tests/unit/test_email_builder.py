import pytest
import base64
import tempfile
import os
from datetime import datetime, timezone, timedelta
from pathlib import Path

from mailersend.builders.email import EmailBuilder
from mailersend.models.email import (
    EmailRequest, EmailContact, EmailAttachment,
    EmailPersonalization, EmailTrackingSettings, EmailHeader
)
from mailersend.exceptions import ValidationError


class TestEmailBuilder:
    """Test EmailBuilder functionality"""
    
    def test_simple_email_construction(self):
        """Test building a simple email"""
        email = (EmailBuilder()
            .from_email("sender@example.com", "Sender")
            .to("recipient@example.com", "Recipient")
            .subject("Test Subject")
            .html("<h1>Test</h1>")
            .build())
        
        assert isinstance(email, EmailRequest)
        assert email.from_email.email == "sender@example.com"
        assert email.from_email.name == "Sender"
        assert len(email.to) == 1
        assert email.to[0].email == "recipient@example.com"
        assert email.to[0].name == "Recipient"
        assert email.subject == "Test Subject"
        assert email.html == "<h1>Test</h1>"
    
    def test_multiple_recipients(self):
        """Test adding multiple recipients"""
        email = (EmailBuilder()
            .from_email("sender@example.com")
            .to("user1@example.com", "User 1")
            .to("user2@example.com", "User 2")
            .cc("cc@example.com", "CC User")
            .bcc("bcc@example.com")
            .subject("Multiple Recipients")
            .text("Test message")
            .build())
        
        assert len(email.to) == 2
        assert email.to[0].email == "user1@example.com"
        assert email.to[1].email == "user2@example.com"
        assert len(email.cc) == 1
        assert email.cc[0].email == "cc@example.com"
        assert len(email.bcc) == 1
        assert email.bcc[0].email == "bcc@example.com"
    
    def test_to_many_recipients(self):
        """Test adding multiple recipients at once"""
        recipients = [
            {"email": "user1@example.com", "name": "User 1"},
            {"email": "user2@example.com", "name": "User 2"},
            {"email": "user3@example.com"}  # No name
        ]
        
        email = (EmailBuilder()
            .from_email("sender@example.com")
            .to_many(recipients)
            .subject("Bulk Recipients")
            .text("Test message")
            .build())
        
        assert len(email.to) == 3
        assert email.to[0].email == "user1@example.com"
        assert email.to[0].name == "User 1"
        assert email.to[1].email == "user2@example.com"
        assert email.to[1].name == "User 2"
        assert email.to[2].email == "user3@example.com"
        assert email.to[2].name is None
    
    def test_content_methods(self):
        """Test different content setting methods"""
        email = (EmailBuilder()
            .from_email("sender@example.com")
            .to("recipient@example.com")
            .subject("Content Test")
            .html("<h1>HTML Content</h1>")
            .text("Plain text content")
            .build())
        
        assert email.html == "<h1>HTML Content</h1>"
        assert email.text == "Plain text content"
    
    def test_file_content_methods(self):
        """Test loading content from files"""
        # Create temporary files
        html_content = "<h1>File HTML</h1><p>From file</p>"
        text_content = "File text content"
        
        with tempfile.TemporaryDirectory() as temp_dir:
            html_file = Path(temp_dir) / "test.html"
            text_file = Path(temp_dir) / "test.txt"
            
            html_file.write_text(html_content)
            text_file.write_text(text_content)
            
            email = (EmailBuilder()
                .from_email("sender@example.com")
                .to("recipient@example.com")
                .subject("File Content Test")
                .html_file(html_file)
                .text_file(text_file)
                .build())
            
            assert email.html == html_content
            assert email.text == text_content
    
    def test_file_content_error_handling(self):
        """Test error handling for file operations"""
        builder = EmailBuilder()
        
        # Test non-existent file
        with pytest.raises(ValidationError, match="Failed to read HTML file"):
            builder.html_file("non_existent_file.html")
        
        with pytest.raises(ValidationError, match="Failed to read text file"):
            builder.text_file("non_existent_file.txt")
    
    def test_template_method(self):
        """Test template ID setting"""
        email = (EmailBuilder()
            .from_email("sender@example.com")
            .to("recipient@example.com")
            .subject("Template Test")
            .template("template-123")
            .build())
        
        assert email.template_id == "template-123"
    
    def test_attach_file(self):
        """Test file attachment"""
        file_content = b"This is test file content"
        
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir) / "test.txt"
            file_path.write_bytes(file_content)
            
            email = (EmailBuilder()
                .from_email("sender@example.com")
                .to("recipient@example.com")
                .subject("Attachment Test")
                .text("Test with attachment")
                .attach_file(file_path, "custom_name.txt", "attachment")
                .build())
            
            assert len(email.attachments) == 1
            attachment = email.attachments[0]
            assert attachment.filename == "custom_name.txt"
            assert attachment.disposition == "attachment"
            # Verify content is base64 encoded
            decoded_content = base64.b64decode(attachment.content)
            assert decoded_content == file_content
    
    def test_attach_file_default_filename(self):
        """Test file attachment with default filename"""
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir) / "original_name.pdf"
            file_path.write_bytes(b"PDF content")
            
            email = (EmailBuilder()
                .from_email("sender@example.com")
                .to("recipient@example.com")
                .subject("Attachment Test")
                .text("Test")
                .attach_file(file_path)
                .build())
            
            assert email.attachments[0].filename == "original_name.pdf"
    
    def test_attach_file_error_handling(self):
        """Test attachment error handling"""
        builder = EmailBuilder()
        
        with pytest.raises(ValidationError, match="File not found"):
            builder.attach_file("non_existent_file.txt")
    
    def test_attach_content(self):
        """Test direct content attachment"""
        content = "Direct attachment content"
        
        email = (EmailBuilder()
            .from_email("sender@example.com")
            .to("recipient@example.com")
            .subject("Direct Attachment Test")
            .text("Test")
            .attach_content(content, "direct.txt", "inline")
            .build())
        
        assert len(email.attachments) == 1
        attachment = email.attachments[0]
        assert attachment.filename == "direct.txt"
        assert attachment.disposition == "inline"
        # Verify content
        decoded_content = base64.b64decode(attachment.content).decode('utf-8')
        assert decoded_content == content
    
    def test_attach_content_bytes(self):
        """Test attaching bytes content"""
        content = b"Binary content"
        
        email = (EmailBuilder()
            .from_email("sender@example.com")
            .to("recipient@example.com")
            .subject("Binary Attachment Test")
            .text("Test")
            .attach_content(content, "binary.dat")
            .build())
        
        attachment = email.attachments[0]
        decoded_content = base64.b64decode(attachment.content)
        assert decoded_content == content
    
    def test_tags(self):
        """Test tag functionality"""
        email = (EmailBuilder()
            .from_email("sender@example.com")
            .to("recipient@example.com")
            .subject("Tag Test")
            .text("Test")
            .tag("tag1", "tag2", "tag3")
            .tag("tag4")
            .build())
        
        assert email.tags == ["tag1", "tag2", "tag3", "tag4"]
    
    def test_personalization(self):
        """Test personalization functionality"""
        email = (EmailBuilder()
            .from_email("sender@example.com")
            .to("user1@example.com")
            .to("user2@example.com")
            .subject("Personalization Test")
            .html("Hello {$name}!")
            .personalize("user1@example.com", name="John", company="Acme")
            .personalize("user2@example.com", name="Jane", role="Manager")
            .build())
        
        assert len(email.personalization) == 2
        assert email.personalization[0].email == "user1@example.com"
        assert email.personalization[0].data == {"name": "John", "company": "Acme"}
        assert email.personalization[1].email == "user2@example.com"
        assert email.personalization[1].data == {"name": "Jane", "role": "Manager"}
    
    def test_personalize_many(self):
        """Test bulk personalization"""
        personalizations = [
            {"email": "user1@example.com", "data": {"name": "John"}},
            {"email": "user2@example.com", "data": {"name": "Jane"}}
        ]
        
        email = (EmailBuilder()
            .from_email("sender@example.com")
            .to("user1@example.com")
            .to("user2@example.com")
            .subject("Bulk Personalization Test")
            .text("Hello {$name}!")
            .personalize_many(personalizations)
            .build())
        
        assert len(email.personalization) == 2
        assert email.personalization[0].email == "user1@example.com"
        assert email.personalization[0].data == {"name": "John"}
    
    def test_scheduling(self):
        """Test email scheduling"""
        # Test with datetime
        send_time = datetime.now(timezone.utc) + timedelta(hours=1)
        
        email = (EmailBuilder()
            .from_email("sender@example.com")
            .to("recipient@example.com")
            .subject("Scheduled Email")
            .text("Scheduled test")
            .send_at(send_time)
            .build())
        
        assert email.send_at == int(send_time.timestamp())
        
        # Test with timestamp
        timestamp = int(send_time.timestamp())
        
        email2 = (EmailBuilder()
            .from_email("sender@example.com")
            .to("recipient@example.com")
            .subject("Scheduled Email 2")
            .text("Scheduled test 2")
            .send_at(timestamp)
            .build())
        
        assert email2.send_at == timestamp
    
    def test_send_in(self):
        """Test relative scheduling"""
        start_time = datetime.now(timezone.utc)
        
        email = (EmailBuilder()
            .from_email("sender@example.com")
            .to("recipient@example.com")
            .subject("Relative Schedule Test")
            .text("Test")
            .send_in(hours=2, minutes=30)
            .build())
        
        expected_time = start_time + timedelta(hours=2, minutes=30)
        # Allow for small time difference in test execution
        assert abs(email.send_at - int(expected_time.timestamp())) < 5
    
    def test_threading(self):
        """Test email threading features"""
        email = (EmailBuilder()
            .from_email("sender@example.com")
            .to("recipient@example.com")
            .subject("Re: Original Subject")
            .text("Reply message")
            .in_reply_to("original@example.com")
            .reference("<ref1@example.com>", "<ref2@example.com>")
            .build())
        
        assert email.in_reply_to == "original@example.com"
        assert email.references == ["<ref1@example.com>", "<ref2@example.com>"]
    
    def test_tracking_individual(self):
        """Test individual tracking settings"""
        email = (EmailBuilder()
            .from_email("sender@example.com")
            .to("recipient@example.com")
            .subject("Tracking Test")
            .text("Test")
            .track_clicks(True)
            .track_opens(False)
            .track_content(True)
            .build())
        
        assert email.settings.track_clicks is True
        assert email.settings.track_opens is False
        assert email.settings.track_content is True
    
    def test_tracking_bulk(self):
        """Test bulk tracking configuration"""
        email = (EmailBuilder()
            .from_email("sender@example.com")
            .to("recipient@example.com")
            .subject("Bulk Tracking Test")
            .text("Test")
            .tracking(clicks=True, opens=False, content=None)
            .build())
        
        assert email.settings.track_clicks is True
        assert email.settings.track_opens is False
        assert email.settings.track_content is None
    
    def test_headers(self):
        """Test custom headers"""
        email = (EmailBuilder()
            .from_email("sender@example.com")
            .to("recipient@example.com")
            .subject("Headers Test")
            .text("Test")
            .header("X-Custom-Header", "Custom Value")
            .headers({"X-Priority": "1", "X-Campaign": "test"})
            .build())
        
        assert len(email.headers) == 3
        header_dict = {h.name: h.value for h in email.headers}
        assert header_dict["X-Custom-Header"] == "Custom Value"
        assert header_dict["X-Priority"] == "1"
        assert header_dict["X-Campaign"] == "test"
    
    def test_bulk_mode(self):
        """Test bulk mode setting"""
        email = (EmailBuilder()
            .from_email("sender@example.com")
            .to("recipient@example.com")
            .subject("Bulk Mode Test")
            .text("Test")
            .bulk_mode(True)
            .build())
        
        assert email.precedence_bulk is True
        
        email2 = (EmailBuilder()
            .from_email("sender@example.com")
            .to("recipient@example.com")
            .subject("Non-Bulk Test")
            .text("Test")
            .bulk_mode(False)
            .build())
        
        assert email2.precedence_bulk is False
    
    def test_reply_to(self):
        """Test reply-to functionality"""
        email = (EmailBuilder()
            .from_email("sender@example.com")
            .to("recipient@example.com")
            .subject("Reply-To Test")
            .text("Test")
            .reply_to("reply@example.com", "Reply Handler")
            .build())
        
        assert email.reply_to.email == "reply@example.com"
        assert email.reply_to.name == "Reply Handler"
    
    def test_builder_reset(self):
        """Test builder reset functionality"""
        builder = (EmailBuilder()
            .from_email("sender@example.com")
            .to("recipient@example.com")
            .subject("Test")
            .text("Test"))
        
        # Reset and build new email
        email = (builder.reset()
            .from_email("new@example.com")
            .to("new_recipient@example.com")
            .subject("New Subject")
            .text("New content")
            .build())
        
        assert email.from_email.email == "new@example.com"
        assert email.to[0].email == "new_recipient@example.com"
        assert email.subject == "New Subject"
    
    def test_builder_copy(self):
        """Test builder copy functionality"""
        original = (EmailBuilder()
            .from_email("sender@example.com")
            .subject("Template Subject")
            .tag("template")
            .track_opens(True))
        
        # Copy and customize
        email1 = (original.copy()
            .to("user1@example.com")
            .text("Message for user 1")
            .build())
        
        email2 = (original.copy()
            .to("user2@example.com")
            .text("Message for user 2")
            .build())
        
        # Both should have template settings
        assert email1.from_email.email == "sender@example.com"
        assert email2.from_email.email == "sender@example.com"
        assert email1.subject == "Template Subject"
        assert email2.subject == "Template Subject"
        assert "template" in email1.tags
        assert "template" in email2.tags
        
        # But different recipients and content
        assert email1.to[0].email == "user1@example.com"
        assert email2.to[0].email == "user2@example.com"
        assert email1.text == "Message for user 1"
        assert email2.text == "Message for user 2"
    
    def test_build_validation_error(self):
        """Test that build() raises ValidationError for invalid configurations"""
        # Missing required fields
        with pytest.raises(ValidationError, match="Failed to build email request"):
            EmailBuilder().build()  # No recipients, subject, or content
    
    def test_complex_email_construction(self):
        """Test building a complex email with all features"""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create test attachment
            attachment_path = Path(temp_dir) / "test.pdf"
            attachment_path.write_bytes(b"PDF content")
            
            email = (EmailBuilder()
                .from_email("marketing@company.com", "Marketing Team")
                .to("customer1@example.com", "Customer 1")
                .to("customer2@example.com", "Customer 2")
                .cc("manager@company.com", "Manager")
                .bcc("analytics@company.com")
                .reply_to("support@company.com", "Support Team")
                .subject("Complex Email Test")
                .html("<h1>Hello {$name}!</h1><p>From {$company}</p>")
                .text("Hello {$name}! From {$company}")
                .attach_file(attachment_path, "report.pdf")
                .personalize("customer1@example.com", name="John", company="Acme Corp")
                .personalize("customer2@example.com", name="Jane", company="Tech Ltd")
                .tag("marketing", "newsletter", "q4")
                .tracking(clicks=True, opens=True, content=False)
                .header("X-Campaign-ID", "newsletter-q4-2024")
                .header("X-Priority", "3")
                .send_in(hours=2)
                .bulk_mode(False)
                .build())
            
            # Verify all components
            assert email.from_email.email == "marketing@company.com"
            assert len(email.to) == 2
            assert len(email.cc) == 1
            assert len(email.bcc) == 1
            assert email.reply_to.email == "support@company.com"
            assert email.subject == "Complex Email Test"
            assert email.html.startswith("<h1>Hello {$name}!")
            assert len(email.attachments) == 1
            assert len(email.personalization) == 2
            assert len(email.tags) == 3
            assert email.settings.track_clicks is True
            assert len(email.headers) == 2
            assert email.send_at is not None
            assert email.precedence_bulk is False 