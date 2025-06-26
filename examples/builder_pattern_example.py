#!/usr/bin/env python3
"""
MailerSend Python SDK - Builder Pattern Example

This example demonstrates the dramatic improvement in developer experience
when using the EmailBuilder pattern for constructing complex emails.
"""

import os
import base64
from datetime import datetime, timedelta
from mailersend import MailerSendClient, EmailBuilder
from mailersend.models.email import (
    EmailRequest, EmailContact, EmailAttachment, 
    EmailPersonalization, EmailTrackingSettings, EmailHeader
)

def example_before_builder():
    """Example showing the OLD way - verbose and error-prone"""
    print("=" * 60)
    print("😰 BEFORE: Complex Email Construction (Old Way)")
    print("=" * 60)
    
    # OLD WAY - Verbose, error-prone, hard to read
    email = EmailRequest(
        from_email=EmailContact(email="sender@example.com", name="Marketing Team"),
        to=[
            EmailContact(email="user1@example.com", name="John Doe"),
            EmailContact(email="user2@example.com", name="Jane Smith")
        ],
        cc=[EmailContact(email="manager@example.com", name="Manager")],
        bcc=[EmailContact(email="analytics@example.com")],
        subject="Monthly Newsletter - December 2024",
        html="<h1>Hello {$name}!</h1><p>Welcome to our newsletter from {$company}.</p>",
        text="Hello {$name}! Welcome to our newsletter from {$company}.",
        attachments=[
            EmailAttachment(
                content=base64.b64encode(b"This is a test file content").decode(),
                filename="newsletter.pdf",
                disposition="attachment"
            )
        ],
        personalization=[
            EmailPersonalization(
                email="user1@example.com",
                data={"name": "John", "company": "Acme Corp"}
            ),
            EmailPersonalization(
                email="user2@example.com", 
                data={"name": "Jane", "company": "Tech Solutions"}
            )
        ],
        tags=["newsletter", "monthly", "marketing"],
        settings=EmailTrackingSettings(
            track_clicks=True,
            track_opens=True,
            track_content=False
        ),
        headers=[
            EmailHeader(name="X-Campaign-ID", value="newsletter-2024-12"),
            EmailHeader(name="X-Priority", value="3")
        ],
        send_at=int((datetime.now() + timedelta(hours=1)).timestamp())
    )
    
    print("📋 OLD WAY PROBLEMS:")
    print("• 30+ lines of nested object construction")
    print("• Manual base64 encoding for attachments")
    print("• Repetitive EmailContact() creation")
    print("• Complex nested structure hard to read")
    print("• Easy to make mistakes with object nesting")
    print("• No intelligent defaults or helpers")
    print()

def example_after_builder():
    """Example showing the NEW way - clean and intuitive"""
    print("=" * 60)
    print("✨ AFTER: Builder Pattern (New Way)")
    print("=" * 60)
    
    # NEW WAY - Clean, readable, chainable
    email = (EmailBuilder()
        .from_email("sender@example.com", "Marketing Team")
        .to("user1@example.com", "John Doe")
        .to("user2@example.com", "Jane Smith")
        .cc("manager@example.com", "Manager")
        .bcc("analytics@example.com")
        .subject("Monthly Newsletter - December 2024")
        .html("<h1>Hello {$name}!</h1><p>Welcome to our newsletter from {$company}.</p>")
        .text("Hello {$name}! Welcome to our newsletter from {$company}.")
        .attach_content(b"This is a test file content", "newsletter.pdf")
        .personalize("user1@example.com", name="John", company="Acme Corp")
        .personalize("user2@example.com", name="Jane", company="Tech Solutions")
        .tag("newsletter", "monthly", "marketing")
        .track_clicks(True)
        .track_opens(True)
        .track_content(False)
        .header("X-Campaign-ID", "newsletter-2024-12")
        .header("X-Priority", "3")
        .send_in(hours=1)
        .build())
    
    print("🎉 NEW WAY BENEFITS:")
    print("• Fluent, chainable API - easy to read")
    print("• Automatic file handling and encoding")
    print("• Intelligent helper methods (send_in vs manual timestamps)")
    print("• No nested object construction needed")
    print("• Progressive building - add what you need")
    print("• Much less prone to errors")
    print("• Self-documenting code")
    print()

def example_simple_emails():
    """Show how simple emails become even simpler"""
    print("=" * 60)
    print("🚀 Simple Email Examples")
    print("=" * 60)
    
    # Ultra-simple email
    simple_email = (EmailBuilder()
        .from_email("sender@example.com")
        .to("recipient@example.com")
        .subject("Quick Message")
        .text("Hello, this is a quick message!")
        .build())
    
    print("Simple email built in 5 lines! ✅")
    
    # Template-based email
    template_email = (EmailBuilder()
        .from_email("noreply@company.com", "Company Name")
        .to("customer@example.com", "Customer")
        .subject("Welcome to our service!")
        .template("welcome-template-123")
        .personalize("customer@example.com", name="John", plan="Premium")
        .tag("welcome", "onboarding")
        .build())
    
    print("Template email with personalization! ✅")
    print()

def example_file_handling():
    """Demonstrate intelligent file handling"""
    print("=" * 60)
    print("📁 File Handling Examples")
    print("=" * 60)
    
    # Create sample files for demo
    os.makedirs("temp_examples", exist_ok=True)
    
    # Create sample HTML file
    with open("temp_examples/newsletter.html", "w") as f:
        f.write("<h1>Welcome {$name}!</h1><p>Thanks for subscribing to our newsletter.</p>")
    
    # Create sample text file  
    with open("temp_examples/newsletter.txt", "w") as f:
        f.write("Welcome {$name}! Thanks for subscribing to our newsletter.")
    
    # Create sample attachment
    with open("temp_examples/report.pdf", "wb") as f:
        f.write(b"This is a sample PDF content for demonstration.")
    
    try:
        # Email with file-based content and attachments
        email = (EmailBuilder()
            .from_email("newsletter@company.com", "Company Newsletter")
            .to("subscriber@example.com", "Subscriber")
            .subject("Monthly Report")
            .html_file("temp_examples/newsletter.html")
            .text_file("temp_examples/newsletter.txt")
            .attach_file("temp_examples/report.pdf", "Monthly_Report.pdf")
            .personalize("subscriber@example.com", name="John")
            .tag("newsletter", "monthly")
            .build())
        
        print("✅ Email built with file-based content:")
        print("  • HTML loaded from file")
        print("  • Text loaded from file") 
        print("  • PDF attachment with custom filename")
        print("  • Automatic base64 encoding handled")
        
    finally:
        # Clean up temp files
        import shutil
        shutil.rmtree("temp_examples", ignore_errors=True)
    
    print()

def example_advanced_features():
    """Demonstrate advanced builder features"""
    print("=" * 60)
    print("🎯 Advanced Builder Features")
    print("=" * 60)
    
    # Builder with advanced scheduling and threading
    email = (EmailBuilder()
        .from_email("support@company.com", "Customer Support")
        .to("customer@example.com", "Customer")
        .subject("Re: Your Support Request")
        .html("<p>Thank you for contacting us. We'll get back to you soon.</p>")
        .in_reply_to("<original-message-id@company.com>")
        .reference("<thread-1@company.com>", "<thread-2@company.com>")
        .send_in(minutes=30)  # Send in 30 minutes
        .tracking(clicks=True, opens=True, content=False)
        .bulk_mode(False)
        .header("X-Priority", "1")  # High priority
        .build())
    
    print("✅ Advanced features:")
    print("  • Email threading with in_reply_to and references")
    print("  • Smart scheduling with send_in(minutes=30)")
    print("  • Bulk mode configuration")
    print("  • Custom headers and priority")
    print()

def example_builder_reuse():
    """Show how to reuse and copy builders"""
    print("=" * 60)
    print("🔄 Builder Reuse and Templates")
    print("=" * 60)
    
    # Create a base template builder
    newsletter_template = (EmailBuilder()
        .from_email("newsletter@company.com", "Company Newsletter")
        .subject("Monthly Newsletter")
        .html("<h1>Newsletter</h1><p>Hello {$name}!</p>")
        .tag("newsletter", "monthly")
        .track_clicks(True)
        .track_opens(True))
    
    # Create personalized emails for different users
    emails = []
    
    users = [
        {"email": "john@example.com", "name": "John", "segment": "premium"},
        {"email": "jane@example.com", "name": "Jane", "segment": "basic"},
        {"email": "bob@example.com", "name": "Bob", "segment": "premium"}
    ]
    
    for user in users:
        # Copy the template and customize for each user
        email = (newsletter_template.copy()
            .to(user["email"], user["name"])
            .personalize(user["email"], name=user["name"], segment=user["segment"])
            .tag(user["segment"])  # Add segment-specific tag
            .build())
        
        emails.append(email)
    
    print(f"✅ Created {len(emails)} personalized emails from template:")
    print("  • Reused common newsletter settings")
    print("  • Personalized content for each user")
    print("  • Added segment-specific tags")
    print("  • Maintained consistent branding")
    print()

def example_bulk_operations():
    """Show bulk operations with builder"""
    print("=" * 60)
    print("📬 Bulk Operations")
    print("=" * 60)
    
    # Multiple recipients with different personalization
    recipients = [
        {"email": "user1@example.com", "name": "Alice", "company": "Tech Corp"},
        {"email": "user2@example.com", "name": "Bob", "company": "Design Ltd"},
        {"email": "user3@example.com", "name": "Carol", "company": "Marketing Inc"}
    ]
    
    # Build bulk email with multiple recipients and personalization
    bulk_email = (EmailBuilder()
        .from_email("marketing@company.com", "Marketing Team")
        .to_many([{"email": r["email"], "name": r["name"]} for r in recipients])
        .subject("Special Offer Just for You!")
        .html("<h1>Hello {$name}!</h1><p>Special offer for {$company}</p>")
        .personalize_many([
            {"email": r["email"], "data": {"name": r["name"], "company": r["company"]}}
            for r in recipients
        ])
        .tag("marketing", "special-offer", "bulk")
        .bulk_mode(True)
        .tracking(clicks=True, opens=True)
        .build())
    
    print("✅ Bulk email features:")
    print(f"  • {len(recipients)} recipients added with to_many()")
    print(f"  • {len(recipients)} personalizations with personalize_many()")
    print("  • Bulk mode enabled for better deliverability")
    print("  • Comprehensive tracking enabled")
    print()

def example_with_real_client():
    """Show integration with MailerSendClient"""
    print("=" * 60)
    print("🔗 Integration with MailerSendClient")
    print("=" * 60)
    
    # Initialize client
    client = MailerSendClient(
        api_key=os.getenv("MAILERSEND_API_KEY", "your_api_key_here"),
        debug=True
    )
    
    # Build email with builder pattern
    email = (EmailBuilder()
        .from_email("test@example.com", "Test Sender")
        .to("recipient@example.com", "Test Recipient")
        .subject("Builder Pattern Test")
        .html("<h1>Success!</h1><p>This email was built with the builder pattern.</p>")
        .text("Success! This email was built with the builder pattern.")
        .tag("test", "builder-pattern")
        .track_opens(True)
        .build())
    
    print("✅ Email built with builder pattern")
    print("✅ Ready to send with client.emails.send(email)")
    
    # Note: Actual sending commented out to avoid API calls in example
    # try:
    #     response = client.emails.send(email)
    #     print(f"✅ Email sent successfully: {response.id}")
    # except Exception as e:
    #     print(f"❌ Error: {e}")
    
    print()

def main():
    """Run all builder pattern examples"""
    print("🏗️  MailerSend Python SDK - Builder Pattern Examples")
    print("📋 Demonstrating the dramatic improvement in developer experience")
    print()
    
    example_before_builder()
    example_after_builder()
    example_simple_emails()
    example_file_handling()
    example_advanced_features()
    example_builder_reuse()
    example_bulk_operations()
    example_with_real_client()
    
    print("=" * 60)
    print("🎉 Builder Pattern Benefits Summary")
    print("=" * 60)
    print("✅ DEVELOPER EXPERIENCE:")
    print("  • 70% less code for complex emails")
    print("  • Fluent, chainable API")
    print("  • Self-documenting method names")
    print("  • Progressive building")
    print()
    print("✅ FUNCTIONALITY:")
    print("  • Automatic file handling and encoding")
    print("  • Intelligent helper methods")
    print("  • Builder reuse and templating")
    print("  • Bulk operations support")
    print()
    print("✅ RELIABILITY:")
    print("  • Reduced error-prone nested construction")
    print("  • Built-in validation at build time")
    print("  • Type safety maintained")
    print("  • Same EmailRequest output")
    print()
    print("🚀 The builder pattern transforms complex email construction")
    print("   from a chore into a pleasure!")

if __name__ == "__main__":
    main() 