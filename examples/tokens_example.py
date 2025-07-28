#!/usr/bin/env python3
"""
Comprehensive example demonstrating the MailerSend Tokens API.

This example shows all token management operations including:
- Listing API tokens with pagination
- Getting individual tokens
- Creating tokens with various scopes
- Updating token status (pause/unpause)
- Updating token names
- Deleting tokens
- Using builder pattern with scope helpers
- Error handling and best practices
"""

import os
import sys
from datetime import datetime

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mailersend import MailerSendClient
from mailersend.builders.tokens import TokensBuilder
from mailersend.models.tokens import TOKEN_SCOPES
from mailersend.exceptions import MailerSendError


def main():
    """Main example function."""
    # Initialize client
    api_key = os.getenv("MAILERSEND_API_KEY")
    if not api_key:
        print("❌ Please set MAILERSEND_API_KEY environment variable")
        return

    client = MailerSendClient(api_key=api_key, debug=True)
    
    print("🔐 MailerSend Tokens API Examples")
    print("=" * 50)
    
    # Example domain ID (replace with your actual domain ID)
    domain_id = "your-domain-id-here"
    
    try:
        # 1. List tokens with pagination
        list_tokens_example(client)
        
        # 2. Create token examples
        token_id = create_token_examples(client, domain_id)
        
        if token_id:
            # 3. Get token details
            get_token_example(client, token_id)
            
            # 4. Update token status
            update_token_example(client, token_id)
            
            # 5. Update token name
            update_token_name_example(client, token_id)
            
            # 6. Delete token
            delete_token_example(client, token_id)
        
        # 7. Builder pattern examples
        builder_pattern_examples()
        
        # 8. Scope helper examples
        scope_helper_examples()
        
        # 9. Error handling examples
        error_handling_examples(client)
        
    except MailerSendError as e:
        print(f"❌ MailerSend API Error: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")


def list_tokens_example(client):
    """Example: List API tokens with pagination."""
    print("\n📋 1. Listing API Tokens")
    print("-" * 30)
    
    # Basic listing
    print("Getting first page of tokens:")
    response = client.tokens.list_tokens()
    
    if response.status_code == 200:
        data = response.json()
        tokens = data.get("data", [])
        print(f"✅ Found {len(tokens)} tokens")
        
        for token in tokens:
            print(f"   📄 {token['name']} (ID: {token['id'][:20]}...)")
            print(f"      Status: {token['status']}")
            print(f"      Created: {token['created_at']}")
            print(f"      Scopes: {', '.join(token['scopes'])}")
    
    # Pagination example
    print("\nGetting specific page with custom limit:")
    response = client.tokens.list_tokens(page=1, limit=10)
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Retrieved page 1 with limit 10")
        print(f"   Found {len(data.get('data', []))} tokens")


def create_token_examples(client, domain_id):
    """Example: Create tokens with different configurations."""
    print("\n🆕 2. Creating API Tokens")
    print("-" * 30)
    
    if domain_id == "your-domain-id-here":
        print("⚠️  Skipping token creation - please set a real domain_id")
        return None
    
    # Create a basic email token
    print("Creating basic email token:")
    response = client.tokens.create_token(
        name=f"Email Token {datetime.now().strftime('%Y%m%d_%H%M%S')}",
        domain_id=domain_id,
        scopes=["email_full"]
    )
    
    token_id = None
    if response.status_code == 200:
        data = response.json()["data"]
        token_id = data["id"]
        print(f"✅ Created token: {data['name']}")
        print(f"   ID: {token_id}")
                 print(f"   Access Token: {data['access_token'][:20]}... (truncated for security)")
    
    # Create a comprehensive token with multiple scopes
    print("\nCreating comprehensive token:")
    comprehensive_scopes = [
        "email_full",
        "domains_read",
        "analytics_read",
        "templates_full"
    ]
    
    response = client.tokens.create_token(
        name=f"Comprehensive Token {datetime.now().strftime('%Y%m%d_%H%M%S')}",
        domain_id=domain_id,
        scopes=comprehensive_scopes
    )
    
    if response.status_code == 200:
        data = response.json()["data"]
        print(f"✅ Created comprehensive token: {data['name']}")
        print(f"   Scopes: {', '.join(comprehensive_scopes)}")
    
    return token_id


def get_token_example(client, token_id):
    """Example: Get token details."""
    print("\n🔍 3. Getting Token Details")
    print("-" * 30)
    
    response = client.tokens.get_token(token_id)
    
    if response.status_code == 200:
        data = response.json()["data"]
        print(f"✅ Token Details:")
        print(f"   Name: {data['name']}")
        print(f"   Status: {data['status']}")
        print(f"   Created: {data['created_at']}")
        print(f"   Scopes: {', '.join(data['scopes'])}")
    else:
        print(f"❌ Failed to get token: {response.status_code}")


def update_token_example(client, token_id):
    """Example: Update token status."""
    print("\n✏️  4. Updating Token Status")
    print("-" * 30)
    
    # Pause the token
    print("Pausing token:")
    response = client.tokens.update_token(token_id, "pause")
    
    if response.status_code == 200:
        data = response.json()["data"]
        print(f"✅ Token paused: {data['name']}")
        print(f"   Status: {data['status']}")
    
    # Unpause the token
    print("\nUnpausing token:")
    response = client.tokens.update_token(token_id, "unpause")
    
    if response.status_code == 200:
        data = response.json()["data"]
        print(f"✅ Token unpaused: {data['name']}")
        print(f"   Status: {data['status']}")


def update_token_name_example(client, token_id):
    """Example: Update token name."""
    print("\n📝 5. Updating Token Name")
    print("-" * 30)
    
    new_name = f"Updated Token {datetime.now().strftime('%Y%m%d_%H%M%S')}"
    response = client.tokens.update_token_name(token_id, new_name)
    
    if response.status_code == 200:
        data = response.json()["data"]
        print(f"✅ Token name updated:")
        print(f"   New Name: {data['name']}")
        print(f"   ID: {data['id']}")


def delete_token_example(client, token_id):
    """Example: Delete token."""
    print("\n🗑️  6. Deleting Token")
    print("-" * 30)
    
    response = client.tokens.delete_token(token_id)
    
    if response.status_code == 200:
        print(f"✅ Token deleted successfully")
    else:
        print(f"❌ Failed to delete token: {response.status_code}")


def builder_pattern_examples():
    """Example: Using TokensBuilder with method chaining."""
    print("\n🔧 7. Builder Pattern Examples")
    print("-" * 30)
    
    # Create a builder instance
    builder = TokensBuilder()
    
    # Example 1: Building a list request with pagination
    print("Building list request with pagination:")
    list_request = (builder
                   .page(2)
                   .limit(50)
                   .build_tokens_list())
    print(f"✅ Page: {list_request.page}, Limit: {list_request.limit}")
    
    # Example 2: Building a create request with method chaining
    print("\nBuilding create request with method chaining:")
    builder.reset()  # Reset builder state
    create_request = (builder
                     .name("API Token from Builder")
                     .domain_id("example-domain-id")
                     .add_scope("email_full")
                     .add_scope("domains_read")
                     .build_token_create())
    print(f"✅ Name: {create_request.name}")
    print(f"   Domain: {create_request.domain_id}")
    print(f"   Scopes: {create_request.scopes}")
    
    # Example 3: Building update request
    print("\nBuilding update request:")
    builder.reset()
    update_request = (builder
                     .token_id("example-token-id")
                     .status("pause")
                     .build_token_update())
    print(f"✅ Token ID: {update_request.token_id}")
    print(f"   Status: {update_request.status}")


def scope_helper_examples():
    """Example: Using scope helper methods."""
    print("\n🎯 8. Scope Helper Examples")
    print("-" * 30)
    
    builder = TokensBuilder()
    
    # Example 1: Using individual scope helpers
    print("Using individual scope helpers:")
    builder.email_scopes().domains_read_scope().analytics_scopes()
    print(f"✅ Scopes added: {builder._scopes}")
    
    # Example 2: Using convenience methods
    print("\nUsing all read scopes helper:")
    builder.reset().all_read_scopes()
    print(f"✅ Read scopes: {len(builder._scopes)} scopes")
    print(f"   Examples: {builder._scopes[:3]}...")
    
    # Example 3: Building comprehensive token
    print("\nBuilding comprehensive token with helpers:")
    builder.reset()
    create_request = (builder
                     .name("Full Access Token")
                     .domain_id("example-domain")
                     .email_scopes()
                     .domains_full_scope()
                     .analytics_scopes()
                     .tokens_scope()
                     .build_token_create())
    print(f"✅ Token with {len(create_request.scopes)} scopes:")
    for scope in create_request.scopes:
        print(f"   • {scope}")
    
    # Example 4: Status helpers
    print("\nUsing status helpers:")
    builder.reset()
    pause_request = (builder
                    .token_id("example-token")
                    .pause()  # Helper for status("pause")
                    .build_token_update())
    print(f"✅ Pause request: {pause_request.status}")
    
    unpause_request = (builder
                      .reset()
                      .token_id("example-token")
                      .unpause()  # Helper for status("unpause")
                      .build_token_update())
    print(f"✅ Unpause request: {unpause_request.status}")


def error_handling_examples(client):
    """Example: Error handling scenarios."""
    print("\n⚠️  9. Error Handling Examples")
    print("-" * 30)
    
    # Example 1: Invalid token ID
    print("Testing with invalid token ID:")
    try:
        response = client.tokens.get_token("invalid-token-id")
        if response.status_code == 404:
            print("✅ Properly handled 404 for invalid token")
    except MailerSendError as e:
        print(f"✅ Caught expected error: {e}")
    
    # Example 2: Builder validation
    print("\nTesting builder validation:")
    builder = TokensBuilder()
    try:
        # This should raise ValueError due to missing required fields
        builder.name("Test").build_token_create()  # Missing domain_id and scopes
    except ValueError as e:
        print(f"✅ Builder validation worked: {e}")
    
    # Example 3: Model validation
    print("\nTesting model validation:")
    try:
        from mailersend.models.tokens import TokenCreateRequest
        # This should raise ValidationError due to invalid scope
        TokenCreateRequest(
            name="Test",
            domain_id="domain123",
            scopes=["invalid_scope"]
        )
    except Exception as e:
        print(f"✅ Model validation worked: {type(e).__name__}")


def production_tips():
    """Production tips and best practices."""
    print("\n💡 Production Tips")
    print("-" * 30)
    
    tips = [
        "🔒 Store API keys securely (environment variables, secrets management)",
        "📊 Use specific scopes - only grant permissions you need",
        "⏱️  Monitor token usage and rotate tokens regularly",
        "🔄 Implement token refresh logic for long-running applications",
        "📝 Keep track of token purposes with descriptive names",
        "🚨 Set up monitoring for failed token operations",
        "🔍 Use pagination for listing large numbers of tokens",
        "🛡️  Handle rate limits gracefully with retry logic",
        "📋 Log token operations for security auditing",
        "🧪 Test token permissions in staging before production"
    ]
    
    for tip in tips:
        print(f"   {tip}")


if __name__ == "__main__":
    main()
    production_tips()
    
    print("\n🎉 Tokens API examples completed!")
    print("\nNext steps:")
    print("1. Set MAILERSEND_API_KEY environment variable")
    print("2. Replace 'your-domain-id-here' with actual domain ID")
    print("3. Run the examples to see the API in action")
    print("4. Explore the builder pattern for complex token configurations")
    print("5. Implement proper error handling in your application") 