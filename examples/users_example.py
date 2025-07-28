#!/usr/bin/env python3
"""
Users API Example

This example demonstrates how to use the MailerSend Users API to:
- Manage account users (list, get, invite, update, delete)
- Manage invites (list, get, resend, cancel)
- Use role helpers and permission groups
- Handle errors and builder patterns

Before running this example, make sure to:
1. Install the mailersend package: pip install mailersend
2. Set your API token in the MAILERSEND_API_TOKEN environment variable
"""

import os
import sys
from typing import List

# Add the parent directory to the path to import mailersend
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mailersend import MailerSend
from mailersend.builders.users import UsersBuilder


def setup_client() -> MailerSend:
    """Initialize the MailerSend client."""
    api_token = os.getenv("MAILERSEND_API_TOKEN")
    if not api_token:
        raise ValueError(
            "Please set your MailerSend API token in the MAILERSEND_API_TOKEN environment variable.\n"
            "You can get your API token from: https://app.mailersend.com/settings/tokens"
        )
    
    return MailerSend(api_token)


def list_users_example(client: MailerSend) -> None:
    """Example: List all account users."""
    print("\n" + "="*50)
    print("LIST USERS EXAMPLE")
    print("="*50)
    
    try:
        response = client.users.list_users()
        print(f"✅ Successfully retrieved users")
        print(f"Status Code: {response.status_code}")
        
        if response.body.get('data'):
            users = response.body['data']
            print(f"Found {len(users)} users:")
            for user in users:
                print(f"  - {user['name']} ({user['email']}) - Role: {user['role']}")
        else:
            print("No users found")
            
    except Exception as e:
        print(f"❌ Error listing users: {e}")


def get_user_example(client: MailerSend, user_id: str) -> None:
    """Example: Get a single user by ID."""
    print("\n" + "="*50)
    print("GET USER EXAMPLE")
    print("="*50)
    
    try:
        response = client.users.get_user(user_id)
        print(f"✅ Successfully retrieved user: {user_id}")
        print(f"Status Code: {response.status_code}")
        
        if response.body.get('data'):
            user = response.body['data']
            print(f"User Details:")
            print(f"  Name: {user.get('name', 'N/A')}")
            print(f"  Email: {user['email']}")
            print(f"  Role: {user['role']}")
            print(f"  2FA: {user.get('2fa', False)}")
            print(f"  Permissions: {len(user.get('permissions', []))}")
            print(f"  Domains: {len(user.get('domains', []))}")
            print(f"  Templates: {len(user.get('templates', []))}")
            
    except Exception as e:
        print(f"❌ Error getting user: {e}")


def invite_user_basic_example(client: MailerSend) -> None:
    """Example: Invite a user with basic settings."""
    print("\n" + "="*50)
    print("INVITE USER - BASIC EXAMPLE")
    print("="*50)
    
    try:
        # Basic invite with Admin role
        response = client.users.invite_user(
            email="new-admin@example.com",
            role="Admin"
        )
        
        print(f"✅ Successfully invited user")
        print(f"Status Code: {response.status_code}")
        
        if response.body.get('data'):
            invite = response.body['data']
            print(f"Invite Details:")
            print(f"  ID: {invite['id']}")
            print(f"  Email: {invite['email']}")
            print(f"  Role: {invite['role']}")
            
    except Exception as e:
        print(f"❌ Error inviting user: {e}")


def invite_user_custom_example(client: MailerSend) -> None:
    """Example: Invite a custom user with specific permissions."""
    print("\n" + "="*50)
    print("INVITE USER - CUSTOM ROLE EXAMPLE")
    print("="*50)
    
    try:
        # Custom user with specific permissions
        response = client.users.invite_user(
            email="custom-user@example.com",
            role="Custom User",
            permissions=[
                "read-all-templates",
                "read-own-templates",
                "manage-template",
                "read-analytics",
                "read-activity"
            ],
            templates=["template1", "template2"],  # Replace with actual template IDs
            domains=["domain1"],  # Replace with actual domain IDs
            requires_periodic_password_change=True
        )
        
        print(f"✅ Successfully invited custom user")
        print(f"Status Code: {response.status_code}")
        
        if response.body.get('data'):
            invite = response.body['data']
            print(f"Invite Details:")
            print(f"  ID: {invite['id']}")
            print(f"  Email: {invite['email']}")
            print(f"  Role: {invite['role']}")
            print(f"  Permissions: {len(invite.get('permissions', []))}")
            print(f"  Periodic Password Change: {invite.get('requires_periodic_password_change')}")
            
    except Exception as e:
        print(f"❌ Error inviting custom user: {e}")


def invite_user_with_builder_example(client: MailerSend) -> None:
    """Example: Use builder pattern for creating user invites."""
    print("\n" + "="*50)
    print("INVITE USER - BUILDER PATTERN EXAMPLE")
    print("="*50)
    
    try:
        # Using builder pattern with role and permission helpers
        builder = UsersBuilder()
        
        # Create a designer with template permissions
        designer_invite = (builder
                          .email("designer@example.com")
                          .designer_role()
                          .template_permissions()
                          .add_permission("read-analytics")  # Add additional permission
                          .requires_periodic_password_change(False))
        
        # Note: In a real application, you would call build_user_invite() and pass to API
        print("✅ Builder created for designer invite")
        print(f"Email: {designer_invite._email}")
        print(f"Role: {designer_invite._role}")
        print(f"Permissions: {designer_invite._permissions}")
        
        # Create another user with multiple permission groups
        manager_builder = (UsersBuilder()
                          .email("manager@example.com")
                          .manager_role())
        
        print("\n✅ Builder created for manager invite")
        print(f"Email: {manager_builder._email}")
        print(f"Role: {manager_builder._role}")
        
        # Copy builder and create variation
        accountant_builder = manager_builder.copy().email("accountant@example.com").accountant_role()
        print(f"\n✅ Copied and modified builder for accountant")
        print(f"Email: {accountant_builder._email}")
        print(f"Role: {accountant_builder._role}")
        
    except Exception as e:
        print(f"❌ Error with builder pattern: {e}")


def update_user_example(client: MailerSend, user_id: str) -> None:
    """Example: Update an existing user."""
    print("\n" + "="*50)
    print("UPDATE USER EXAMPLE")
    print("="*50)
    
    try:
        response = client.users.update_user(
            user_id=user_id,
            role="Manager",
            permissions=[
                "read-analytics",
                "read-activity",
                "manage-template"
            ],
            requires_periodic_password_change=False
        )
        
        print(f"✅ Successfully updated user: {user_id}")
        print(f"Status Code: {response.status_code}")
        
        if response.body.get('data'):
            user = response.body['data']
            print(f"Updated User:")
            print(f"  Email: {user['email']}")
            print(f"  Role: {user['role']}")
            
    except Exception as e:
        print(f"❌ Error updating user: {e}")


def delete_user_example(client: MailerSend, user_id: str) -> None:
    """Example: Delete a user."""
    print("\n" + "="*50)
    print("DELETE USER EXAMPLE")
    print("="*50)
    
    try:
        response = client.users.delete_user(user_id)
        print(f"✅ Successfully deleted user: {user_id}")
        print(f"Status Code: {response.status_code}")
        
    except Exception as e:
        print(f"❌ Error deleting user: {e}")


def list_invites_example(client: MailerSend) -> None:
    """Example: List all pending invites."""
    print("\n" + "="*50)
    print("LIST INVITES EXAMPLE")
    print("="*50)
    
    try:
        response = client.users.list_invites()
        print(f"✅ Successfully retrieved invites")
        print(f"Status Code: {response.status_code}")
        
        if response.body.get('data'):
            invites = response.body['data']
            print(f"Found {len(invites)} pending invites:")
            for invite in invites:
                print(f"  - {invite['email']} - Role: {invite['role']} (ID: {invite['id']})")
        else:
            print("No pending invites found")
            
    except Exception as e:
        print(f"❌ Error listing invites: {e}")


def get_invite_example(client: MailerSend, invite_id: str) -> None:
    """Example: Get a single invite by ID."""
    print("\n" + "="*50)
    print("GET INVITE EXAMPLE")
    print("="*50)
    
    try:
        response = client.users.get_invite(invite_id)
        print(f"✅ Successfully retrieved invite: {invite_id}")
        print(f"Status Code: {response.status_code}")
        
        if response.body.get('data'):
            invite = response.body['data']
            print(f"Invite Details:")
            print(f"  Email: {invite['email']}")
            print(f"  Role: {invite['role']}")
            print(f"  Permissions: {len(invite.get('permissions', []))}")
            if invite.get('data'):
                print(f"  Domains: {len(invite['data'].get('domains', []))}")
                print(f"  Templates: {len(invite['data'].get('templates', []))}")
            
    except Exception as e:
        print(f"❌ Error getting invite: {e}")


def resend_invite_example(client: MailerSend, invite_id: str) -> None:
    """Example: Resend an invite."""
    print("\n" + "="*50)
    print("RESEND INVITE EXAMPLE")
    print("="*50)
    
    try:
        response = client.users.resend_invite(invite_id)
        print(f"✅ Successfully resent invite: {invite_id}")
        print(f"Status Code: {response.status_code}")
        
        if response.body.get('data'):
            invite = response.body['data']
            print(f"Resent invite to: {invite['email']}")
            
    except Exception as e:
        print(f"❌ Error resending invite: {e}")


def cancel_invite_example(client: MailerSend, invite_id: str) -> None:
    """Example: Cancel an invite."""
    print("\n" + "="*50)
    print("CANCEL INVITE EXAMPLE")
    print("="*50)
    
    try:
        response = client.users.cancel_invite(invite_id)
        print(f"✅ Successfully canceled invite: {invite_id}")
        print(f"Status Code: {response.status_code}")
        
    except Exception as e:
        print(f"❌ Error canceling invite: {e}")


def permission_helpers_example() -> None:
    """Example: Demonstrate permission helper methods."""
    print("\n" + "="*50)
    print("PERMISSION HELPERS EXAMPLE")
    print("="*50)
    
    builder = UsersBuilder()
    
    # Template permissions
    builder.template_permissions()
    print("Template Permissions:")
    for perm in builder._permissions:
        print(f"  - {perm}")
    
    # Reset and try domain permissions
    builder.reset().domain_permissions()
    print("\nDomain Permissions:")
    for perm in builder._permissions:
        print(f"  - {perm}")
    
    # Reset and try analytics permissions
    builder.reset().analytics_permissions()
    print("\nAnalytics Permissions:")
    for perm in builder._permissions:
        print(f"  - {perm}")
    
    # Reset and try account permissions
    builder.reset().account_permissions()
    print("\nAccount Permissions:")
    for perm in builder._permissions:
        print(f"  - {perm}")
    
    # Combine multiple permission groups
    builder.reset().template_permissions().analytics_permissions()
    print(f"\nCombined Template + Analytics: {len(builder._permissions)} permissions")


def error_handling_example(client: MailerSend) -> None:
    """Example: Demonstrate error handling."""
    print("\n" + "="*50)
    print("ERROR HANDLING EXAMPLE")
    print("="*50)
    
    try:
        # Try to get a non-existent user
        response = client.users.get_user("non-existent-user-id")
        print(f"Response status: {response.status_code}")
        
        if response.status_code == 404:
            print("✅ Properly handled 404 - User not found")
        elif response.status_code >= 400:
            print(f"❌ API error: {response.status_code}")
            if hasattr(response, 'body') and response.body:
                print(f"Error details: {response.body}")
        else:
            print("✅ Unexpected success - user found")
            
    except Exception as e:
        print(f"❌ Exception occurred: {e}")
    
    try:
        # Try to invite user with invalid email (will be caught by validation)
        builder = UsersBuilder()
        builder.email("invalid-email").role("Admin").build_user_invite()
        
    except ValueError as e:
        print(f"✅ Validation error caught: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")


def main():
    """Run all examples."""
    print("MailerSend Users API Examples")
    print("=" * 50)
    
    try:
        # Initialize the client
        client = setup_client()
        print("✅ MailerSend client initialized successfully")
        
        # Run examples
        list_users_example(client)
        
        # Note: Replace these with actual IDs from your account for testing
        # get_user_example(client, "your-user-id-here")
        # update_user_example(client, "your-user-id-here")
        # delete_user_example(client, "your-user-id-here")
        
        invite_user_basic_example(client)
        invite_user_custom_example(client)
        invite_user_with_builder_example(client)
        
        list_invites_example(client)
        
        # Note: Replace these with actual invite IDs from your account for testing
        # get_invite_example(client, "your-invite-id-here")
        # resend_invite_example(client, "your-invite-id-here")
        # cancel_invite_example(client, "your-invite-id-here")
        
        permission_helpers_example()
        error_handling_example(client)
        
        print("\n" + "="*50)
        print("EXAMPLES COMPLETED")
        print("="*50)
        print("\n📝 Production Tips:")
        print("  1. Always validate email addresses before inviting users")
        print("  2. Use Custom User role for granular permissions")
        print("  3. Regularly review and clean up pending invites")
        print("  4. Implement proper error handling for API calls")
        print("  5. Use builder pattern for complex user setups")
        print("  6. Consider periodic password changes for security")
        print("  7. Monitor user activity and permissions regularly")
        
    except Exception as e:
        print(f"❌ Error running examples: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 