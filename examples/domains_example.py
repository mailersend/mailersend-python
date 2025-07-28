#!/usr/bin/env python3
"""
MailerSend Domains API Example

This example demonstrates how to use the MailerSend Domains API to:
- List domains with filtering and pagination
- Create new domains
- Get single domain information
- Update domain settings
- Manage domain recipients
- Retrieve DNS records
- Check verification status
- Delete domains

This showcases the complete 4-layer architecture with models, builders, resources, and error handling.
"""

import os
import sys
from typing import List

# Add the parent directory to the path so we can import mailersend
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from mailersend import MailerSendClient, DomainsBuilder
from mailersend.models.domains import DomainCreateRequest, DomainUpdateSettingsRequest
from mailersend.exceptions import MailerSendError, ValidationError


def main():
    """Demonstrate various Domains API operations."""
    
    # Initialize the client
    api_key = os.getenv("MAILERSEND_API_KEY")
    if not api_key:
        print("❌ Please set MAILERSEND_API_KEY environment variable")
        return
    
    client = MailerSendClient(api_key=api_key, debug=True)
    print("✅ MailerSend client initialized\n")
    
    try:
        # === 1. LIST DOMAINS ===
        print("🔍 Listing all domains...")
        list_request = DomainsBuilder().limit(10).build_list_request()
        domains_response = client.domains.list_domains(list_request)
        
        print(f"Found {len(domains_response.data['data'])} domains")
        for domain in domains_response.data['data']:
            status = "✅ Verified" if domain['is_verified'] else "⚠️ Unverified"
            print(f"  - {domain['name']} (ID: {domain['id']}) - {status}")
        print()
        
        # === 2. LIST ONLY VERIFIED DOMAINS ===
        print("🔍 Listing only verified domains...")
        verified_request = (DomainsBuilder()
            .verified_only()
            .limit(5)
            .build_list_request())
        
        verified_response = client.domains.list_domains(verified_request)
        print(f"Found {len(verified_response.data['data'])} verified domains")
        print()
        
        # === 3. CREATE NEW DOMAIN (Example - will fail without real domain) ===
        print("➕ Creating a new domain...")
        try:
            create_request = (DomainsBuilder()
                .domain_name("example-test.com")
                .return_path_subdomain("mail")
                .custom_tracking_subdomain("track")
                .inbound_routing_subdomain("inbox")
                .build_create_request())
            
            created_domain = client.domains.create_domain(create_request)
            print(f"✅ Domain created: {created_domain.data['data']['name']}")
            new_domain_id = created_domain.data['data']['id']
        except MailerSendError as e:
            print(f"⚠️ Domain creation failed (expected): {e}")
            # Use an existing domain for the rest of the example
            if domains_response.data['data']:
                new_domain_id = domains_response.data['data'][0]['id']
                print(f"📍 Using existing domain: {domains_response.data['data'][0]['name']}")
            else:
                print("❌ No domains available for further examples")
                return
        print()
        
        # === 4. GET SINGLE DOMAIN ===
        print(f"🔍 Getting domain details for: {new_domain_id}")
        domain_response = client.domains.get_domain(new_domain_id)
        domain = domain_response.data['data']
        
        print(f"Domain: {domain['name']}")
        print(f"Verified: {'✅ Yes' if domain['is_verified'] else '❌ No'}")
        print(f"DKIM: {'✅' if domain.get('dkim') else '❌'}")
        print(f"SPF: {'✅' if domain.get('spf') else '❌'}")
        print()
        
        # === 5. UPDATE DOMAIN SETTINGS ===
        print(f"⚙️ Updating domain settings...")
        try:
            settings_request = (DomainsBuilder()
                .track_opens(True)
                .track_clicks(True)
                .track_content(False)
                .custom_tracking_enabled(True)
                .build_update_settings_request())
            
            updated_domain = client.domains.update_domain_settings(new_domain_id, settings_request)
            print("✅ Domain settings updated successfully")
            
            settings = updated_domain.data['data']['domain_settings']
            print(f"  Track Opens: {'✅' if settings['track_opens'] else '❌'}")
            print(f"  Track Clicks: {'✅' if settings['track_clicks'] else '❌'}")
            print(f"  Track Content: {'✅' if settings['track_content'] else '❌'}")
        except MailerSendError as e:
            print(f"⚠️ Settings update failed: {e}")
        print()
        
        # === 6. GET DOMAIN RECIPIENTS ===
        print(f"👥 Getting domain recipients...")
        try:
            recipients_request = (DomainsBuilder()
                .page(1)
                .limit(10)
                .build_recipients_request())
            
            recipients_response = client.domains.get_domain_recipients(new_domain_id, recipients_request)
            recipients = recipients_response.data['data']
            
            print(f"Found {len(recipients)} recipients:")
            for recipient in recipients[:3]:  # Show first 3
                print(f"  - {recipient['email']} (ID: {recipient['id']})")
            if len(recipients) > 3:
                print(f"  ... and {len(recipients) - 3} more")
        except MailerSendError as e:
            print(f"⚠️ Recipients retrieval failed: {e}")
        print()
        
        # === 7. GET DNS RECORDS ===
        print(f"🌐 Getting DNS records...")
        try:
            dns_response = client.domains.get_domain_dns_records(new_domain_id)
            dns_data = dns_response.data['data']
            
            print("DNS Records:")
            if dns_data.get('spf'):
                print(f"  SPF: {dns_data['spf']['hostname']} -> {dns_data['spf']['value'][:50]}...")
            if dns_data.get('dkim'):
                print(f"  DKIM: {dns_data['dkim']['hostname']} -> {dns_data['dkim']['value'][:50]}...")
            if dns_data.get('return_path'):
                print(f"  Return Path: {dns_data['return_path']['hostname']} -> {dns_data['return_path']['value']}")
        except MailerSendError as e:
            print(f"⚠️ DNS records retrieval failed: {e}")
        print()
        
        # === 8. GET VERIFICATION STATUS ===
        print(f"🔒 Checking verification status...")
        try:
            verification_response = client.domains.get_domain_verification_status(new_domain_id)
            verification = verification_response.data['data']
            
            print(f"Verification Status: {verification_response.data['message']}")
            print(f"  DKIM: {'✅' if verification['dkim'] else '❌'}")
            print(f"  SPF: {'✅' if verification['spf'] else '❌'}")
            print(f"  MX: {'✅' if verification['mx'] else '❌'}")
            print(f"  Tracking: {'✅' if verification['tracking'] else '❌'}")
        except MailerSendError as e:
            print(f"⚠️ Verification status check failed: {e}")
        print()
        
        # === 9. BUILDER FLUENT API SHOWCASE ===
        print("🔧 Demonstrating builder fluent API...")
        
        # Complex domain list request
        complex_request = (DomainsBuilder()
            .verified_only()
            .limit(50)
            .page(1)
            .build_list_request())
        
        # Domain creation with all options
        full_create_request = (DomainsBuilder()
            .domain_name("my-new-domain.com")
            .return_path_subdomain("bounce")
            .custom_tracking_subdomain("links")
            .inbound_routing_subdomain("mail")
            .build_create_request())
        
        # Comprehensive settings update
        full_settings_request = (DomainsBuilder()
            .enable_all_tracking()
            .custom_tracking_enabled(True)
            .precedence_bulk(False)
            .ignore_duplicated_recipients(True)
            .track_unsubscribe_html("<p><a href=\"{{unsubscribe}}\">Unsubscribe</a></p>")
            .track_unsubscribe_plain("Unsubscribe: {{unsubscribe}}")
            .build_update_settings_request())
        
        print("✅ All builder examples created successfully")
        print("   - Complex list request with verification filter")
        print("   - Full domain creation request")
        print("   - Comprehensive settings update request")
        print()
        
        # === 10. VALIDATION EXAMPLES ===
        print("🧪 Testing validation...")
        
        try:
            # Invalid domain name (uppercase)
            invalid_request = DomainCreateRequest(name="INVALID-DOMAIN.COM")
        except ValidationError as e:
            print(f"✅ Validation caught invalid domain: {e}")
        
        try:
            # Invalid limit (too high)
            invalid_list = DomainsBuilder().limit(150).build_list_request()
        except ValidationError as e:
            print(f"✅ Builder validation caught invalid limit: {e}")
        print()
        
        print("🎉 All Domains API examples completed successfully!")
        
    except Exception as e:
        print(f"❌ Unexpected error: {e}")


if __name__ == "__main__":
    main() 