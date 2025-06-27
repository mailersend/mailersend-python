"""
Example demonstrating the Webhooks API usage.

This example shows how to:
1. List webhooks for a domain
2. Create a new webhook
3. Get webhook details
4. Update a webhook
5. Delete a webhook
6. Use the builder pattern for easy request construction
"""

import logging
from typing import List, Optional

from mailersend import MailerSendClient
from mailersend.builders import WebhooksBuilder
from mailersend.models.webhooks import (
    WebhookCreateRequest,
    WebhookDeleteRequest,
    WebhookGetRequest,
    WebhookUpdateRequest,
    WebhooksListRequest,
)

# Set up logging to see what's happening
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize client
# In practice, set your API key via environment variable: MAILERSEND_API_KEY
client = MailerSendClient(api_key="your_api_key_here")


def list_webhooks_example(domain_id: str):
    """Example: List all webhooks for a domain."""
    logger.info("=== Listing Webhooks ===")
    
    # Method 1: Using request model directly
    request = WebhooksListRequest(domain_id=domain_id)
    response = client.webhooks.list_webhooks(request)
    
    logger.info(f"Response status: {response.status_code}")
    if response.is_success():
        logger.info(f"Found {len(response.data.get('data', []))} webhooks")
    
    # Method 2: Using builder pattern
    builder = WebhooksBuilder()
    request = builder.domain_id(domain_id).build_webhooks_list_request()
    response = client.webhooks.list_webhooks(request)
    
    logger.info(f"Webhooks listed successfully: {response.is_success()}")
    return response


def create_webhook_example(domain_id: str, webhook_url: str, webhook_name: str):
    """Example: Create a new webhook."""
    logger.info("=== Creating Webhook ===")
    
    # Method 1: Using request model directly
    request = WebhookCreateRequest(
        url=webhook_url,
        name=webhook_name,
        events=["activity.sent", "activity.delivered", "activity.opened"],
        domain_id=domain_id,
        enabled=True
    )
    response = client.webhooks.create_webhook(request)
    
    logger.info(f"Response status: {response.status_code}")
    if response.is_success():
        webhook_data = response.data.get("data", {})
        webhook_id = webhook_data.get("id")
        logger.info(f"Created webhook with ID: {webhook_id}")
        return webhook_id
    
    return None


def create_webhook_with_builder_example(domain_id: str, webhook_url: str, webhook_name: str):
    """Example: Create webhook using builder pattern."""
    logger.info("=== Creating Webhook with Builder ===")
    
    # Using builder with fluent interface
    builder = WebhooksBuilder()
    request = (builder
               .domain_id(domain_id)
               .url(webhook_url)
               .name(webhook_name)
               .activity_events()  # Add all activity events
               .enabled(True)
               .build_webhook_create_request())
    
    response = client.webhooks.create_webhook(request)
    
    logger.info(f"Webhook created: {response.is_success()}")
    if response.is_success():
        webhook_data = response.data.get("data", {})
        return webhook_data.get("id")
    
    return None


def create_webhook_all_events_example(domain_id: str, webhook_url: str, webhook_name: str):
    """Example: Create webhook with all available events."""
    logger.info("=== Creating Webhook with All Events ===")
    
    builder = WebhooksBuilder()
    request = (builder
               .domain_id(domain_id)
               .url(webhook_url)
               .name(webhook_name)
               .all_events()  # Add all available events (activity + system)
               .enabled(True)
               .build_webhook_create_request())
    
    response = client.webhooks.create_webhook(request)
    
    if response.is_success():
        webhook_data = response.data.get("data", {})
        webhook_id = webhook_data.get("id")
        events = webhook_data.get("events", [])
        logger.info(f"Created webhook {webhook_id} with {len(events)} events")
        return webhook_id
    
    return None


def get_webhook_example(webhook_id: str):
    """Example: Get webhook details."""
    logger.info("=== Getting Webhook Details ===")
    
    # Method 1: Using request model directly
    request = WebhookGetRequest(webhook_id=webhook_id)
    response = client.webhooks.get_webhook(request)
    
    logger.info(f"Response status: {response.status_code}")
    if response.is_success():
        webhook_data = response.data.get("data", {})
        logger.info(f"Webhook name: {webhook_data.get('name')}")
        logger.info(f"Webhook URL: {webhook_data.get('url')}")
        logger.info(f"Enabled: {webhook_data.get('enabled')}")
        logger.info(f"Events: {len(webhook_data.get('events', []))}")
    
    # Method 2: Using builder pattern
    builder = WebhooksBuilder()
    request = builder.webhook_id(webhook_id).build_webhook_get_request()
    response = client.webhooks.get_webhook(request)
    
    logger.info(f"Webhook retrieved: {response.is_success()}")
    return response


def update_webhook_example(webhook_id: str):
    """Example: Update webhook."""
    logger.info("=== Updating Webhook ===")
    
    # Method 1: Using request model directly
    request = WebhookUpdateRequest(
        webhook_id=webhook_id,
        name="Updated Webhook Name",
        events=["activity.sent", "activity.delivered", "activity.bounced"],
        enabled=False
    )
    response = client.webhooks.update_webhook(request)
    
    logger.info(f"Response status: {response.status_code}")
    logger.info(f"Webhook updated: {response.is_success()}")
    
    return response


def update_webhook_with_builder_example(webhook_id: str):
    """Example: Update webhook using builder pattern."""
    logger.info("=== Updating Webhook with Builder ===")
    
    # Partial update - only change enabled status
    builder = WebhooksBuilder()
    request = (builder
               .webhook_id(webhook_id)
               .enabled(True)
               .build_webhook_update_request())
    
    response = client.webhooks.update_webhook(request)
    
    logger.info(f"Webhook enabled: {response.is_success()}")
    return response


def update_webhook_events_example(webhook_id: str):
    """Example: Update webhook events only."""
    logger.info("=== Updating Webhook Events ===")
    
    builder = WebhooksBuilder()
    request = (builder
               .webhook_id(webhook_id)
               .system_events()  # Change to system events only
               .build_webhook_update_request())
    
    response = client.webhooks.update_webhook(request)
    
    if response.is_success():
        logger.info("Webhook events updated to system events only")
    
    return response


def delete_webhook_example(webhook_id: str):
    """Example: Delete webhook."""
    logger.info("=== Deleting Webhook ===")
    
    # Method 1: Using request model directly
    request = WebhookDeleteRequest(webhook_id=webhook_id)
    response = client.webhooks.delete_webhook(request)
    
    logger.info(f"Response status: {response.status_code}")
    logger.info(f"Webhook deleted: {response.is_success()}")
    
    # Method 2: Using builder pattern
    builder = WebhooksBuilder()
    request = builder.webhook_id(webhook_id).build_webhook_delete_request()
    response = client.webhooks.delete_webhook(request)
    
    return response


def builder_reuse_example(domain_id: str):
    """Example: Reusing builder for multiple operations."""
    logger.info("=== Builder Reuse Example ===")
    
    # Create a builder and reuse it for different operations
    builder = WebhooksBuilder()
    builder.domain_id(domain_id)
    
    # List webhooks
    list_request = builder.build_webhooks_list_request()
    response = client.webhooks.list_webhooks(list_request)
    logger.info(f"Listed webhooks: {response.is_success()}")
    
    # Add webhook_id and get details (simulating getting first webhook)
    if response.is_success() and response.data.get("data"):
        webhook_id = response.data["data"][0]["id"]
        builder.webhook_id(webhook_id)
        
        get_request = builder.build_webhook_get_request()
        response = client.webhooks.get_webhook(get_request)
        logger.info(f"Got webhook details: {response.is_success()}")
        
        # Update the webhook (builder state is preserved)
        builder.name("Updated via Reused Builder")
        update_request = builder.build_webhook_update_request()
        response = client.webhooks.update_webhook(update_request)
        logger.info(f"Updated webhook: {response.is_success()}")


def builder_copy_example(domain_id: str):
    """Example: Copying builder state."""
    logger.info("=== Builder Copy Example ===")
    
    # Create base builder with common settings
    base_builder = WebhooksBuilder()
    base_builder.domain_id(domain_id)
    base_builder.url("https://example.com/webhook")
    base_builder.enabled(True)
    
    # Create different webhooks with different event sets
    activity_builder = base_builder.copy()
    activity_builder.name("Activity Events Webhook")
    activity_builder.activity_events()
    
    system_builder = base_builder.copy()
    system_builder.name("System Events Webhook")
    system_builder.system_events()
    
    # Create both webhooks
    activity_request = activity_builder.build_webhook_create_request()
    system_request = system_builder.build_webhook_create_request()
    
    # Note: In real usage, you'd call the API here
    logger.info("Created two different webhook configurations from base builder")


def complete_webhook_lifecycle_example():
    """Example: Complete webhook lifecycle."""
    logger.info("=== Complete Webhook Lifecycle ===")
    
    # Replace with your actual domain ID
    domain_id = "your_domain_id_here"
    webhook_url = "https://your-domain.com/webhook"
    webhook_name = "Test Lifecycle Webhook"
    
    try:
        # 1. List existing webhooks
        list_response = list_webhooks_example(domain_id)
        
        # 2. Create a new webhook
        webhook_id = create_webhook_with_builder_example(domain_id, webhook_url, webhook_name)
        
        if webhook_id:
            # 3. Get webhook details
            get_webhook_example(webhook_id)
            
            # 4. Update webhook
            update_webhook_with_builder_example(webhook_id)
            
            # 5. Update webhook events
            update_webhook_events_example(webhook_id)
            
            # 6. Delete webhook
            delete_webhook_example(webhook_id)
            
            logger.info("✅ Complete webhook lifecycle completed successfully!")
        else:
            logger.error("❌ Failed to create webhook")
            
    except Exception as e:
        logger.error(f"❌ Error in webhook lifecycle: {e}")


def webhook_signature_verification_example():
    """Example: Webhook signature verification (conceptual)."""
    logger.info("=== Webhook Signature Verification ===")
    
    # This is a conceptual example of how you would verify webhooks
    # In practice, this would be in your webhook endpoint handler
    
    def verify_webhook_signature(payload: str, signature: str, signing_secret: str) -> bool:
        """
        Verify webhook signature.
        
        Args:
            payload: Raw webhook payload
            signature: Signature from webhook headers
            signing_secret: Your webhook signing secret
            
        Returns:
            bool: True if signature is valid
        """
        import hmac
        import hashlib
        
        # Create HMAC hash
        expected_signature = hmac.new(
            signing_secret.encode('utf-8'),
            payload.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        
        # Compare signatures
        return hmac.compare_digest(signature, expected_signature)
    
    # Example usage in your webhook handler
    webhook_payload = '{"type": "activity.sent", "data": {...}}'
    webhook_signature = "signature_from_header"
    webhook_secret = "your_webhook_signing_secret"
    
    is_valid = verify_webhook_signature(webhook_payload, webhook_signature, webhook_secret)
    logger.info(f"Webhook signature valid: {is_valid}")


if __name__ == "__main__":
    # Enable debug logging for detailed request/response information
    client = MailerSendClient(api_key="your_api_key_here", debug=True)
    
    logger.info("🚀 Starting Webhooks API Examples")
    
    # Run examples (replace with your actual domain ID)
    domain_id = "your_domain_id_here"
    
    # Basic examples
    list_webhooks_example(domain_id)
    
    # Builder pattern examples
    builder_reuse_example(domain_id)
    builder_copy_example(domain_id)
    
    # Signature verification example
    webhook_signature_verification_example()
    
    # Uncomment to run complete lifecycle (requires valid domain_id)
    # complete_webhook_lifecycle_example()
    
    logger.info("✅ Webhooks API examples completed!")
    
    print("""
    📚 Key Takeaways:
    
    1. **List Webhooks**: Use WebhooksListRequest with domain_id
    2. **Create Webhooks**: Specify URL, name, events, and domain_id
    3. **Update Webhooks**: All fields except webhook_id are optional
    4. **Delete Webhooks**: Only webhook_id is required
    5. **Builder Pattern**: Use WebhooksBuilder for fluent interface
    6. **Event Helpers**: Use activity_events(), system_events(), or all_events()
    7. **Builder Reuse**: Copy builders to create variations
    8. **Security**: Always verify webhook signatures in production
    
    🔗 Webhook Events Available:
    - Activity: sent, delivered, bounced, opened, clicked, unsubscribed, etc.
    - System: sender_identity.verified, maintenance.start/end, etc.
    
    📖 For more information, visit: https://developers.mailersend.com/api/v1/webhooks.html
    """) 