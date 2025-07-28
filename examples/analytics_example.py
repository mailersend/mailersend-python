#!/usr/bin/env python3
"""
MailerSend Python SDK - Analytics API Example

This example demonstrates how to use the Analytics API to retrieve
analytics data for email campaigns with the Builder pattern.
"""

import os
from datetime import datetime, timedelta
from mailersend import MailerSendClient, AnalyticsBuilder

def example_activity_by_date():
    """Example: Get activity data grouped by date"""
    print("=" * 60)
    print("📊 Analytics: Activity Data by Date")
    print("=" * 60)
    
    # Build analytics request for the last 7 days
    request = (AnalyticsBuilder()
        .date_range_days(7)  # Last 7 days
        .events("sent", "delivered", "opened", "clicked")  # Track key events
        .group_by("days")  # Group by days
        .tags("newsletter", "marketing")  # Filter by tags
        .build())
    
    print("✅ Request built:")
    print(f"  • Date range: Last 7 days")
    print(f"  • Events: sent, delivered, opened, clicked")
    print(f"  • Group by: days")
    print(f"  • Tags: newsletter, marketing")
    print()
    
    # Using the fluent builder with helper methods
    request2 = (AnalyticsBuilder()
        .this_month()  # This month
        .engagement_events()  # Opened, clicked, opened_unique, clicked_unique
        .group_by("weeks")  # Group by weeks
        .build())
    
    print("✅ Alternative request built:")
    print(f"  • Date range: This month")
    print(f"  • Events: All engagement events")
    print(f"  • Group by: weeks")
    print()

def example_opens_by_country():
    """Example: Get opens data grouped by country"""
    print("=" * 60)
    print("🌍 Analytics: Opens by Country")
    print("=" * 60)
    
    # Build analytics request for country data
    request = (AnalyticsBuilder()
        .date_range_days(30)  # Last 30 days
        .domain("my-domain-id")  # Filter by domain
        .tags("international", "campaign")  # Filter by tags
        .build())
    
    print("✅ Request built:")
    print(f"  • Date range: Last 30 days")
    print(f"  • Domain: my-domain-id")
    print(f"  • Tags: international, campaign")
    print()

def example_opens_by_user_agent():
    """Example: Get opens data grouped by user agent"""
    print("=" * 60)
    print("🔍 Analytics: Opens by User Agent")
    print("=" * 60)
    
    # Build analytics request for user agent data
    request = (AnalyticsBuilder()
        .yesterday()  # Yesterday's data
        .tags("tech-newsletter")  # Filter by tag
        .build())
    
    print("✅ Request built:")
    print(f"  • Date range: Yesterday")
    print(f"  • Tags: tech-newsletter")
    print()

def example_opens_by_reading_environment():
    """Example: Get opens data grouped by reading environment"""
    print("=" * 60)
    print("📱 Analytics: Opens by Reading Environment")
    print("=" * 60)
    
    # Build analytics request for reading environment data
    request = (AnalyticsBuilder()
        .this_week()  # This week
        .tags("mobile-campaign")  # Filter by tag
        .build())
    
    print("✅ Request built:")
    print(f"  • Date range: This week")
    print(f"  • Tags: mobile-campaign")
    print()

def example_advanced_date_filtering():
    """Example: Advanced date filtering options"""
    print("=" * 60)
    print("🗓️ Advanced Date Filtering")
    print("=" * 60)
    
    # Various date filtering options
    examples = [
        ("Today", lambda: AnalyticsBuilder().today()),
        ("Yesterday", lambda: AnalyticsBuilder().yesterday()),
        ("This week", lambda: AnalyticsBuilder().this_week()),
        ("This month", lambda: AnalyticsBuilder().this_month()),
        ("Last 3 days", lambda: AnalyticsBuilder().date_range_days(3)),
        ("Last 2 weeks", lambda: AnalyticsBuilder().date_range_weeks(2)),
        ("Last 3 months", lambda: AnalyticsBuilder().date_range_months(3)),
    ]
    
    for description, builder_func in examples:
        builder = builder_func()
        request = builder.events("sent", "delivered").build()
        print(f"✅ {description}:")
        print(f"  • From: {datetime.fromtimestamp(request.date_from)}")
        print(f"  • To: {datetime.fromtimestamp(request.date_to)}")
        print()

def example_event_helpers():
    """Example: Using event helper methods"""
    print("=" * 60)
    print("🎯 Event Helper Methods")
    print("=" * 60)
    
    # Different event helper methods
    examples = [
        ("All events", lambda b: b.all_events()),
        ("Delivery events", lambda b: b.delivery_events()),
        ("Engagement events", lambda b: b.engagement_events()),
        ("Negative events", lambda b: b.negative_events()),
        ("Custom events", lambda b: b.events("sent", "opened", "clicked")),
    ]
    
    for description, event_func in examples:
        builder = AnalyticsBuilder().date_range_days(7)
        request = event_func(builder).build()
        print(f"✅ {description}:")
        print(f"  • Events: {', '.join(request.event or [])}")
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
        # Build analytics request
        request = (AnalyticsBuilder()
            .date_range_days(7)
            .events("sent", "delivered", "opened")
            .group_by("days")
            .build())
        
        # Make API calls
        print("🔄 Making API calls...")
        
        # Activity by date
        date_response = client.analytics.get_activity_by_date(request)
        print(f"✅ Activity by date: {len(date_response.data.get('stats', []))} data points")
        
        # Opens by country
        country_response = client.analytics.get_opens_by_country(request)
        print(f"✅ Opens by country: {len(country_response.data.get('stats', []))} countries")
        
        # Opens by user agent
        ua_response = client.analytics.get_opens_by_user_agent(request)
        print(f"✅ Opens by user agent: {len(ua_response.data.get('stats', []))} user agents")
        
        # Opens by reading environment
        env_response = client.analytics.get_opens_by_reading_environment(request)
        print(f"✅ Opens by reading environment: {len(env_response.data.get('stats', []))} environments")
        
    except Exception as e:
        print(f"❌ Error: {e}")

def example_builder_reuse():
    """Example: Reusing and copying builders"""
    print("=" * 60)
    print("🔄 Builder Reuse and Copying")
    print("=" * 60)
    
    # Create a base builder
    base_builder = (AnalyticsBuilder()
        .date_range_days(30)
        .tags("newsletter"))
    
    # Copy and customize for different endpoints
    date_request = (base_builder.copy()
        .events("sent", "delivered", "opened")
        .group_by("days")
        .build())
    
    country_request = base_builder.copy().build()
    
    print("✅ Base builder created and copied:")
    print(f"  • Date request events: {', '.join(date_request.event or [])}")
    print(f"  • Country request tags: {', '.join(country_request.tags or [])}")
    print()
    
    # Reset builder for reuse
    base_builder.reset()
    new_request = (base_builder
        .today()
        .events("clicked")
        .build())
    
    print("✅ Builder reset and reused:")
    print(f"  • New request events: {', '.join(new_request.event or [])}")
    print()

def main():
    """Run all examples"""
    print("🎉 MailerSend Analytics API Examples")
    print("=" * 60)
    
    example_activity_by_date()
    example_opens_by_country()
    example_opens_by_user_agent()
    example_opens_by_reading_environment()
    example_advanced_date_filtering()
    example_event_helpers()
    example_builder_reuse()
    
    print("\n🔧 Advanced Usage:")
    example_with_real_client()
    
    print("\n" + "=" * 60)
    print("✨ Analytics API Implementation Complete!")
    print("=" * 60)
    print()
    print("📝 Key Features:")
    print("• ✅ Unified model for all analytics endpoints")
    print("• ✅ Fluent builder with intelligent date helpers")
    print("• ✅ Event helper methods for common use cases")
    print("• ✅ Proper validation and error handling")
    print("• ✅ Type safety with Pydantic models")
    print("• ✅ Comprehensive logging and debugging")
    print()
    print("🚀 Usage Examples:")
    print("• Activity data by date with custom events")
    print("• Opens by country with domain filtering")
    print("• Opens by user agent and reading environment")
    print("• Advanced date filtering (today, yesterday, this week, etc.)")
    print("• Event helpers (all, delivery, engagement, negative)")
    print("• Builder reuse and copying for efficiency")

if __name__ == "__main__":
    main() 