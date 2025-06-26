#!/usr/bin/env python3
"""
MailerSend Python SDK - Enhanced Logging Example

This example demonstrates how to use the enhanced logging capabilities
for debugging issues with your MailerSend integration.
"""

import os
import logging
import time
from mailersend import MailerSendClient, setup_debug_logging
from mailersend.models.email import EmailRequest, EmailContact

def example_basic_debug():
    """Example 1: Basic debug logging with individual client"""
    print("=" * 60)
    print("🔍 Example 1: Basic Debug Logging")
    print("=" * 60)
    
    # Initialize client with debug enabled
    client = MailerSendClient(
        api_key=os.getenv("MAILERSEND_API_KEY", "your_api_key_here"),
        debug=True  # This enables detailed logging for this client
    )
    
    # Create a simple email
    email = EmailRequest(
        to=[EmailContact(email="recipient@example.com", name="John Doe")],
        subject="Debug Test Email",
        text="This is a test email for debugging",
        **{"from": EmailContact(email="sender@yourdomain.com", name="Your Name")}
    )
    
    try:
        response = client.emails.send(email)
        print(f"✅ Email sent: {response.id}")
    except Exception as e:
        print(f"❌ Error: {type(e).__name__}: {e}")

def example_global_debug():
    """Example 2: Global debug logging for entire SDK"""
    print("\n" + "=" * 60)
    print("🌍 Example 2: Global Debug Logging")
    print("=" * 60)
    
    # Enable debug logging for ALL SDK components
    setup_debug_logging()
    
    # Now all clients will have detailed logging
    client = MailerSendClient(
        api_key=os.getenv("MAILERSEND_API_KEY", "your_api_key_here")
    )
    
    # This will show detailed logs even though debug=False in constructor
    try:
        # Example of bulk send
        emails = [
            EmailRequest(
                to=[EmailContact(email=f"user{i}@example.com")],
                subject=f"Bulk Email {i}",
                text=f"This is bulk email number {i}",
                **{"from": EmailContact(email="sender@yourdomain.com")}
            )
            for i in range(2)
        ]
        
        response = client.emails.send_bulk(emails)
        print(f"✅ Bulk emails sent: {response.id}")
    except Exception as e:
        print(f"❌ Error: {type(e).__name__}: {e}")

def example_runtime_debug_control():
    """Example 3: Runtime debug control"""
    print("\n" + "=" * 60)
    print("🎛️  Example 3: Runtime Debug Control")
    print("=" * 60)
    
    client = MailerSendClient(
        api_key=os.getenv("MAILERSEND_API_KEY", "your_api_key_here"),
        debug=False  # Start with debug off
    )
    
    print("Debug info:", client.get_debug_info())
    
    # Enable debug when needed
    print("\n🔧 Enabling debug mode...")
    client.enable_debug()
    
    # Now this request will be logged in detail
    email = EmailRequest(
        to=[EmailContact(email="debug@example.com")],
        subject="Runtime Debug Test",
        html="<h1>Debug Test</h1><p>Testing runtime debug control</p>",
        **{"from": EmailContact(email="sender@yourdomain.com")}
    )
    
    try:
        response = client.emails.send(email)
        print(f"✅ Email sent with debug: {response.id}")
    except Exception as e:
        print(f"❌ Error: {type(e).__name__}: {e}")
    
    # Disable debug
    print("\n🔇 Disabling debug mode...")
    client.disable_debug()

def example_custom_logging():
    """Example 4: Custom logging configuration"""
    print("\n" + "=" * 60)
    print("📝 Example 4: Custom Logging Configuration")
    print("=" * 60)
    
    # Create custom logger
    custom_logger = logging.getLogger("my_app.mailersend")
    custom_logger.setLevel(logging.INFO)
    
    # Custom handler with file output
    handler = logging.FileHandler("mailersend_debug.log")
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    handler.setFormatter(formatter)
    custom_logger.addHandler(handler)
    
    # Use custom logger
    client = MailerSendClient(
        api_key=os.getenv("MAILERSEND_API_KEY", "your_api_key_here"),
        logger=custom_logger,
        debug=True
    )
    
    print("Custom logger configured - check 'mailersend_debug.log' file")
    
    try:
        email = EmailRequest(
            to=[EmailContact(email="custom@example.com")],
            subject="Custom Logger Test",
            text="Testing custom logger configuration",
            **{"from": EmailContact(email="sender@yourdomain.com")}
        )
        
        response = client.emails.send(email)
        print(f"✅ Email sent with custom logger: {response.id}")
    except Exception as e:
        print(f"❌ Error: {type(e).__name__}: {e}")

def example_error_debugging():
    """Example 5: Error debugging scenarios"""
    print("\n" + "=" * 60)
    print("🐛 Example 5: Error Debugging Scenarios")
    print("=" * 60)
    
    client = MailerSendClient(
        api_key="invalid_api_key_for_testing",  # Intentionally invalid
        debug=True
    )
    
    # Test 1: Authentication error
    print("\n🧪 Testing authentication error...")
    try:
        email = EmailRequest(
            to=[EmailContact(email="test@example.com")],
            subject="Auth Error Test",
            text="This should fail with auth error",
            **{"from": EmailContact(email="sender@yourdomain.com")}
        )
        response = client.emails.send(email)
    except Exception as e:
        print(f"Expected error captured: {type(e).__name__}: {e}")
    
    # Test 2: Validation error
    print("\n🧪 Testing validation error...")
    try:
        invalid_email = EmailRequest(
            to=[],  # Empty recipients - should fail validation
            subject="Validation Error Test",
            text="This should fail validation"
        )
        response = client.emails.send(invalid_email)
    except Exception as e:
        print(f"Expected validation error: {type(e).__name__}: {e}")

def example_performance_monitoring():
    """Example 6: Performance monitoring with logging"""
    print("\n" + "=" * 60)
    print("⚡ Example 6: Performance Monitoring")
    print("=" * 60)
    
    client = MailerSendClient(
        api_key=os.getenv("MAILERSEND_API_KEY", "your_api_key_here"),
        debug=True
    )
    
    print("Performance monitoring enabled - watch for timing in logs")
    
    # Simulate multiple requests to monitor performance
    for i in range(3):
        try:
            email = EmailRequest(
                to=[EmailContact(email=f"perf{i}@example.com")],
                subject=f"Performance Test {i+1}",
                text=f"Performance monitoring test email {i+1}",
                **{"from": EmailContact(email="sender@yourdomain.com")}
            )
            
            start_time = time.time()
            response = client.emails.send(email)
            duration = time.time() - start_time
            
            print(f"Request {i+1}: {duration:.3f}s")
            
        except Exception as e:
            print(f"Request {i+1} failed: {type(e).__name__}: {e}")
        
        # Small delay between requests
        time.sleep(0.5)

def main():
    """Run all debugging examples"""
    print("🚀 MailerSend Python SDK - Enhanced Logging Examples")
    print("📋 These examples show various debugging scenarios and configurations")
    print("\n⚠️  Note: Replace 'your_api_key_here' with your actual MailerSend API key")
    print("   Set MAILERSEND_API_KEY environment variable for automatic detection")
    
    # Run examples
    example_basic_debug()
    example_global_debug()
    example_runtime_debug_control()
    example_custom_logging()
    example_error_debugging()
    example_performance_monitoring()
    
    print("\n" + "=" * 60)
    print("✅ All debugging examples completed!")
    print("=" * 60)
    
    print("\n🎯 Key Takeaways:")
    print("• Use debug=True for detailed request/response logging")
    print("• setup_debug_logging() enables debugging for entire SDK")
    print("• Runtime control: client.enable_debug() / client.disable_debug()")
    print("• Custom loggers can be used for file output or custom formats")
    print("• All sensitive data (API keys, tokens) is automatically redacted")
    print("• Each request gets a unique ID for tracking across logs")
    print("• Response timing is automatically measured and logged")

if __name__ == "__main__":
    main() 