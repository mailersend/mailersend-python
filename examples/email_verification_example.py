"""
Email Verification API Examples for MailerSend Python SDK

This example demonstrates how to use the Email Verification API to:
- Verify single emails (sync and async)
- Create and manage verification lists
- Filter and retrieve verification results
- Use the builder pattern for flexible request construction

API Documentation:
https://developers.mailersend.com/api/v1/email-verification.html
"""

import os
import time
from typing import List, Optional

from mailersend import MailerSendClient
from mailersend.builders.email_verification import EmailVerificationBuilder
from mailersend.models.email_verification import (
    EmailVerifyRequest,
    EmailVerifyAsyncRequest,
    EmailVerificationCreateRequest,
    EmailVerificationResultsRequest,
)


def single_email_verification_example(client: MailerSendClient):
    """Example: Verify a single email address (synchronous)."""
    print("\n=== Single Email Verification (Sync) ===")
    
    # Method 1: Direct request model
    request = EmailVerifyRequest(email="test@example.com")
    response = client.email_verification.verify_email(request)
    
    print(f"Email verification status: {response.json()}")
    
    # Method 2: Using builder pattern
    builder = EmailVerificationBuilder()
    request = builder.email("another@example.com").build_verify_email()
    response = client.email_verification.verify_email(request)
    
    print(f"Builder verification status: {response.json()}")


def async_email_verification_example(client: MailerSendClient):
    """Example: Verify a single email address (asynchronous)."""
    print("\n=== Single Email Verification (Async) ===")
    
    # Start async verification
    builder = EmailVerificationBuilder()
    request = builder.email("async@example.com").build_verify_email_async()
    response = client.email_verification.verify_email_async(request)
    
    verification_data = response.json()
    verification_id = verification_data.get("id")
    print(f"Async verification started: {verification_data}")
    
    # Check status (you would typically do this in a loop with delays)
    if verification_id:
        status_request = builder.email_verification_id(verification_id).build_async_status()
        status_response = client.email_verification.get_async_status(status_request)
        print(f"Verification status: {status_response.json()}")


def verification_lists_example(client: MailerSendClient):
    """Example: Create and manage email verification lists."""
    print("\n=== Email Verification Lists ===")
    
    # Create a verification list
    emails_to_verify = [
        "valid@gmail.com",
        "typo@gmial.com",  # Intentional typo
        "nonexistent@invaliddomain123.com",
        "role@company.com"
    ]
    
    builder = EmailVerificationBuilder()
    create_request = (builder
                     .name("Example Verification List")
                     .emails(emails_to_verify)
                     .build_create())
    
    create_response = client.email_verification.create_verification(create_request)
    list_data = create_response.json().get("data", {})
    list_id = list_data.get("id")
    
    print(f"Created verification list: {list_data}")
    
    if list_id:
        # Get the verification list details
        get_request = builder.email_verification_id(list_id).build_get()
        get_response = client.email_verification.get_verification(get_request)
        print(f"List details: {get_response.json()}")
        
        # Start verification process
        verify_request = builder.email_verification_id(list_id).build_verify_list()
        verify_response = client.email_verification.verify_list(verify_request)
        print(f"Verification started: {verify_response.json()}")
        
        # Note: In a real scenario, you would wait for verification to complete
        # before fetching results. This might take several minutes.
        
        return list_id
    
    return None


def list_all_verifications_example(client: MailerSendClient):
    """Example: List all email verification lists with pagination."""
    print("\n=== List All Verification Lists ===")
    
    # List first page
    builder = EmailVerificationBuilder()
    list_request = builder.page(1).limit(25).build_lists()
    response = client.email_verification.list_verifications(list_request)
    
    data = response.json()
    print(f"Verification lists (page 1): {len(data.get('data', []))} lists")
    
    # Check pagination
    meta = data.get("meta", {})
    if meta.get("current_page", 1) < meta.get("last_page", 1):
        # Get next page
        next_page_request = builder.page(2).build_lists()
        next_response = client.email_verification.list_verifications(next_page_request)
        print(f"Next page data: {next_response.json()}")


def verification_results_example(client: MailerSendClient, list_id: str):
    """Example: Get and filter verification results."""
    print("\n=== Verification Results ===")
    
    if not list_id:
        print("No list ID provided, skipping results example")
        return
    
    builder = EmailVerificationBuilder()
    
    # Get all results
    all_results_request = builder.email_verification_id(list_id).build_results()
    all_response = client.email_verification.get_results(all_results_request)
    print(f"All results: {all_response.json()}")
    
    # Filter by valid emails only
    valid_results_request = (builder
                           .email_verification_id(list_id)
                           .valid_results()
                           .build_results())
    valid_response = client.email_verification.get_results(valid_results_request)
    print(f"Valid emails only: {valid_response.json()}")
    
    # Filter by risky emails
    risky_results_request = (builder
                           .reset()  # Clear previous state
                           .email_verification_id(list_id)
                           .risky_results()
                           .build_results())
    risky_response = client.email_verification.get_results(risky_results_request)
    print(f"Risky emails: {risky_response.json()}")
    
    # Filter by 'do not send' emails
    do_not_send_request = (builder
                          .reset()
                          .email_verification_id(list_id)
                          .do_not_send_results()
                          .build_results())
    do_not_send_response = client.email_verification.get_results(do_not_send_request)
    print(f"Do not send emails: {do_not_send_response.json()}")


def builder_advanced_usage_example():
    """Example: Advanced builder pattern usage and state management."""
    print("\n=== Advanced Builder Usage ===")
    
    # Create a base builder configuration
    base_builder = EmailVerificationBuilder()
    base_builder.page(1).limit(50)
    
    # Copy for different scenarios
    email_builder = base_builder.copy().email("test@example.com")
    list_builder = base_builder.copy().email_verification_id("abc123")
    
    # Build different request types
    email_request = email_builder.build_verify_email()
    status_request = list_builder.build_async_status()
    results_request = list_builder.all_results().build_results()
    
    print(f"Email verification request: {email_request}")
    print(f"Status check request: {status_request}")
    print(f"Results request with all filters: {results_request}")
    
    # Demonstrate method chaining and reset
    chained_builder = (EmailVerificationBuilder()
                      .name("Chained List")
                      .add_email("email1@example.com")
                      .add_email("email2@example.com")
                      .add_email("email3@example.com"))
    
    create_request = chained_builder.build_create()
    print(f"Chained creation request: {create_request}")
    
    # Reset and reuse
    chained_builder.reset().email("single@example.com")
    single_request = chained_builder.build_verify_email()
    print(f"After reset, single email request: {single_request}")


def result_categories_example():
    """Example: Understanding email verification result categories."""
    print("\n=== Email Verification Result Categories ===")
    
    # Valid emails (safe to send)
    valid_emails = [
        "valid" # Email is safe to send
    ]
    
    # Risky emails (may cause issues)
    risky_emails = [
        "catch_all",     # Server accepts all emails, but may not be real
        "mailbox_full",  # Recipient's inbox is full
        "role_based",    # Role-based email (support@, info@, etc.)
        "unknown"        # Unable to determine validity
    ]
    
    # Do not send emails (will cause problems)
    do_not_send_emails = [
        "syntax_error",      # Invalid email format
        "typo",             # Email has a typo
        "mailbox_not_found", # Mailbox doesn't exist
        "disposable",       # Temporary/disposable email
        "mailbox_blocked"   # Mailbox is blocked
    ]
    
    print("Valid categories:", valid_emails)
    print("Risky categories:", risky_emails)
    print("Do not send categories:", do_not_send_emails)
    
    # Show how to filter by categories using builder
    builder = EmailVerificationBuilder()
    
    # Get only valid emails
    valid_filter = builder.valid_results().build_results.__doc__ or "Filter for valid emails"
    print(f"Valid filter: {valid_filter}")
    
    # Get risky emails
    builder.reset().risky_results()
    risky_filter = builder._results
    print(f"Risky filters: {risky_filter}")
    
    # Get do not send emails
    builder.reset().do_not_send_results()
    do_not_send_filter = builder._results
    print(f"Do not send filters: {do_not_send_filter}")


def error_handling_example(client: MailerSendClient):
    """Example: Proper error handling for email verification."""
    print("\n=== Error Handling ===")
    
    try:
        # Try to verify an email without sufficient credits
        request = EmailVerifyRequest(email="test@example.com")
        response = client.email_verification.verify_email(request)
        print(f"Verification successful: {response.json()}")
        
    except Exception as e:
        # Handle various error types
        error_type = type(e).__name__
        print(f"Error occurred ({error_type}): {str(e)}")
        
        # Different error handling based on error type
        if "credits" in str(e).lower():
            print("💡 Tip: Check your account balance and add more credits")
        elif "401" in str(e):
            print("🔑 Tip: Check your API key configuration")
        elif "429" in str(e):
            print("⏱️ Tip: You're hitting rate limits, slow down requests")
        else:
            print("❓ Check the API documentation for more details")


def main():
    """Main example function demonstrating email verification features."""
    # Initialize the client
    api_key = os.getenv("MAILERSEND_API_KEY")
    if not api_key:
        print("❌ Please set the MAILERSEND_API_KEY environment variable")
        print("   You can get your API key from: https://app.mailersend.com/")
        return
    
    # Enable debug mode for detailed logging
    client = MailerSendClient(api_key=api_key, debug=True)
    
    print("🔍 MailerSend Email Verification API Examples")
    print("=" * 50)
    
    try:
        # Run examples
        single_email_verification_example(client)
        async_email_verification_example(client)
        
        # Create a verification list and get its ID
        list_id = verification_lists_example(client)
        
        list_all_verifications_example(client)
        
        # Note: In a real scenario, you'd wait for verification to complete
        # before checking results. For demo purposes, we'll try anyway.
        if list_id:
            print("\n⚠️ Note: Verification may still be in progress...")
            verification_results_example(client, list_id)
        
        # Educational examples
        builder_advanced_usage_example()
        result_categories_example()
        error_handling_example(client)
        
        print("\n✅ Email verification examples completed!")
        print("\n💡 Tips for production use:")
        print("   • Wait for list verification to complete before checking results")
        print("   • Implement webhook handling for async notifications")
        print("   • Monitor your credit usage and set up alerts")
        print("   • Use appropriate result filtering based on your use case")
        print("   • Consider batch processing for large email lists")
        
    except Exception as e:
        print(f"\n❌ Example failed: {e}")
        print("   Check your API key and network connection")


if __name__ == "__main__":
    main() 