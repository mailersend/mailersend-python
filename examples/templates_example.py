#!/usr/bin/env python3
"""
MailerSend Python SDK - Templates API Example

This example demonstrates how to use the Templates API to manage
email templates with the Builder pattern.
"""

import os
from mailersend import MailerSendClient
from mailersend.builders.templates import TemplatesBuilder
from mailersend.models.templates import (
    TemplatesListRequest, TemplateGetRequest, TemplateDeleteRequest
)


def example_list_templates():
    """Example: List all templates"""
    print("=" * 60)
    print("📄 Templates: List All Templates")
    print("=" * 60)
    
    # Build templates list request with default settings
    request = (TemplatesBuilder()
        .all()  # All templates (no domain filter)
        .first_page()  # Start from page 1
        .default_limit()  # Use default limit (25)
        .build_templates_list_request())
    
    print("✅ Request built:")
    print(f"  • Domain filter: {request.domain_id}")
    print(f"  • Page: {request.page}")
    print(f"  • Limit: {request.limit}")
    print()


def example_list_templates_with_filters():
    """Example: List templates with domain filter and pagination"""
    print("=" * 60)
    print("📄 Templates: List with Filters")
    print("=" * 60)
    
    # Build templates list request with domain filter
    request = (TemplatesBuilder()
        .domain_id("your-domain-id")  # Filter by specific domain
        .page(2)  # Second page
        .limit(50)  # 50 templates per page
        .build_templates_list_request())
    
    print("✅ Request built:")
    print(f"  • Domain filter: {request.domain_id}")
    print(f"  • Page: {request.page}")
    print(f"  • Limit: {request.limit}")
    print()


def example_get_single_template():
    """Example: Get a single template by ID"""
    print("=" * 60)
    print("📄 Templates: Get Single Template")
    print("=" * 60)
    
    # Build template get request
    request = (TemplatesBuilder()
        .template_id("your-template-id")
        .build_template_get_request())
    
    print("✅ Request built:")
    print(f"  • Template ID: {request.template_id}")
    print()


def example_delete_template():
    """Example: Delete a template"""
    print("=" * 60)
    print("📄 Templates: Delete Template")
    print("=" * 60)
    
    # Build template delete request
    request = (TemplatesBuilder()
        .template_id("template-to-delete")
        .build_template_delete_request())
    
    print("✅ Request built:")
    print(f"  • Template ID: {request.template_id}")
    print()


def example_pagination_workflow():
    """Example: Template pagination workflow"""
    print("=" * 60)
    print("📄 Templates: Pagination Workflow")
    print("=" * 60)
    
    # Start with minimum page size
    builder = TemplatesBuilder()
    
    # First page with minimum limit
    first_page = (builder
        .first_page()
        .min_limit()  # 10 templates per page
        .build_templates_list_request())
    
    print("✅ First page request:")
    print(f"  • Page: {first_page.page}")
    print(f"  • Limit: {first_page.limit}")
    
    # Next page with maximum limit
    next_page = (builder
        .page(2)
        .max_limit()  # 100 templates per page
        .build_templates_list_request())
    
    print("✅ Next page request:")
    print(f"  • Page: {next_page.page}")
    print(f"  • Limit: {next_page.limit}")
    print()


def example_builder_reuse():
    """Example: Builder reuse and copying"""
    print("=" * 60)
    print("📄 Templates: Builder Reuse")
    print("=" * 60)
    
    # Create a base builder for a specific domain
    base_builder = (TemplatesBuilder()
        .domain_id("my-domain")
        .default_limit())
    
    # Use copy for different pages
    page1_request = (base_builder
        .copy()  # Create a copy
        .page(1)
        .build_templates_list_request())
    
    page2_request = (base_builder
        .copy()  # Create another copy
        .page(2)
        .build_templates_list_request())
    
    print("✅ Page 1 request:")
    print(f"  • Domain: {page1_request.domain_id}")
    print(f"  • Page: {page1_request.page}")
    
    print("✅ Page 2 request:")
    print(f"  • Domain: {page2_request.domain_id}")
    print(f"  • Page: {page2_request.page}")
    
    # Reset builder for different use case
    different_request = (base_builder
        .reset()  # Clear all settings
        .template_id("specific-template")
        .build_template_get_request())
    
    print("✅ Different request after reset:")
    print(f"  • Template ID: {different_request.template_id}")
    print()


def example_direct_model_usage():
    """Example: Using models directly without builder"""
    print("=" * 60)
    print("📄 Templates: Direct Model Usage")
    print("=" * 60)
    
    # Create requests directly
    list_request = TemplatesListRequest(
        domain_id="direct-domain",
        page=1,
        limit=25
    )
    
    get_request = TemplateGetRequest(
        template_id="direct-template-id"
    )
    
    delete_request = TemplateDeleteRequest(
        template_id="template-to-delete"
    )
    
    print("✅ Direct list request:")
    print(f"  • Domain: {list_request.domain_id}")
    print(f"  • Page: {list_request.page}")
    print(f"  • Limit: {list_request.limit}")
    
    print("✅ Direct get request:")
    print(f"  • Template ID: {get_request.template_id}")
    
    print("✅ Direct delete request:")
    print(f"  • Template ID: {delete_request.template_id}")
    print()


def example_with_real_client():
    """Example: Using with real MailerSend client"""
    print("=" * 60)
    print("🚀 Real API Usage")
    print("=" * 60)
    
    # Get API key from environment
    api_key = os.getenv("MAILERSEND_API_KEY")
    if not api_key:
        print("⚠️  Set MAILERSEND_API_KEY environment variable to run real API examples")
        print("   Example: export MAILERSEND_API_KEY='your-api-key-here'")
        return
    
    # Initialize client
    client = MailerSendClient(api_key=api_key, debug=True)
    
    try:
        # List templates
        print("🔄 Listing templates...")
        list_request = (TemplatesBuilder()
            .first_page()
            .limit(10)
            .build_templates_list_request())
        
        templates_response = client.templates.list_templates(list_request)
        print(f"✅ Found {len(templates_response.data)} templates")
        
        # Show first template if available
        if templates_response.data:
            first_template = templates_response.data[0]
            print(f"   First template: {first_template.name} (ID: {first_template.id})")
            
            # Get detailed template information
            print("🔄 Getting template details...")
            get_request = (TemplatesBuilder()
                .template_id(first_template.id)
                .build_template_get_request())
            
            template_response = client.templates.get_template(get_request)
            template = template_response.data
            
            print("✅ Template details:")
            print(f"   • Name: {template.name}")
            print(f"   • Type: {template.type}")
            print(f"   • Created: {template.created_at}")
            if template.category:
                print(f"   • Category: {template.category.name}")
            if template.domain:
                print(f"   • Domain: {template.domain.name}")
            if template.template_stats:
                print(f"   • Total sent: {template.template_stats.total}")
        
    except Exception as e:
        print(f"❌ Error: {e}")


def main():
    """Run all examples"""
    print("🎉 MailerSend Templates API Examples")
    print("=" * 60)
    
    example_list_templates()
    example_list_templates_with_filters()
    example_get_single_template()
    example_delete_template()
    example_pagination_workflow()
    example_builder_reuse()
    example_direct_model_usage()
    
    print("\n🔧 Advanced Usage:")
    example_with_real_client()
    
    print("\n" + "=" * 60)
    print("✨ Templates API Implementation Complete!")
    print("=" * 60)
    print()
    print("📝 Key Features:")
    print("• ✅ List templates with domain filtering and pagination")
    print("• ✅ Get detailed template information including stats")
    print("• ✅ Delete templates with proper error handling")
    print("• ✅ Fluent builder interface with helper methods")
    print("• ✅ Comprehensive validation and error handling")
    print("• ✅ Type safety with Pydantic models")
    print("• ✅ Builder reuse and copying for efficiency")
    print()
    print("🚀 Usage Examples:")
    print("• List all templates with default pagination")
    print("• Filter templates by domain with custom page size")
    print("• Get single template with full details and statistics")
    print("• Delete templates with validation")
    print("• Advanced pagination workflows")
    print("• Builder pattern reuse and state management")


if __name__ == "__main__":
    main() 