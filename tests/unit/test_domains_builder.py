"""
Unit tests for Domains builder.

Tests builder fluent API, validation, state management, and all helper methods.
"""

import pytest
from pydantic import ValidationError

from mailersend.builders.domains import DomainsBuilder
from mailersend.models.domains import (
    DomainListRequest,
    DomainCreateRequest,
    DomainDeleteRequest,
    DomainUpdateSettingsRequest,
    DomainRecipientsRequest,
    DomainGetRequest,
    DomainDnsRecordsRequest,
    DomainVerificationRequest
)
from mailersend.exceptions import ValidationError as MailerSendValidationError


class TestDomainsBuilderBasicOperations:
    """Test basic DomainsBuilder operations."""
    
    def test_builder_initialization(self):
        """Test builder initializes with clean state."""
        builder = DomainsBuilder()
        
        # Check initial state is empty
        assert builder._page is None
        assert builder._limit is None
        assert builder._verified is None
        assert builder._name is None
        assert builder._return_path_subdomain is None
        assert builder._custom_tracking_subdomain is None
        assert builder._inbound_routing_subdomain is None
        assert builder._domain_id is None
        
        # Check settings state is empty
        assert builder._send_paused is None
        assert builder._track_opens is None
        assert builder._track_clicks is None
    
    def test_builder_fluent_interface(self):
        """Test that all methods return builder instance for chaining."""
        builder = DomainsBuilder()
        
        # Test method chaining returns same instance
        result = (builder
                 .page(1)
                 .limit(10)
                 .verified(True)
                 .domain_name("test.com")
                 .track_opens(True))
        
        assert result is builder
    
    def test_reset_method(self):
        """Test reset method clears all state."""
        builder = DomainsBuilder()
        
        # Set various fields
        builder.page(2).limit(50).verified(True).domain_name("test.com").track_opens(True)
        
        # Verify state is set
        assert builder._page == 2
        assert builder._limit == 50
        assert builder._verified is True
        assert builder._name == "test.com"
        assert builder._track_opens is True
        
        # Reset and verify clean state
        builder.reset()
        
        assert builder._page is None
        assert builder._limit is None
        assert builder._verified is None
        assert builder._name is None
        assert builder._track_opens is None
    
    def test_copy_method(self):
        """Test copy method creates independent instance."""
        original = DomainsBuilder()
        original.page(1).limit(25).verified(True).domain_name("test.com").domain_id("domain-123")
        
        # Create copy
        copy_builder = original.copy()
        
        # Verify copy has same state
        assert copy_builder._page == 1
        assert copy_builder._limit == 25
        assert copy_builder._verified is True
        assert copy_builder._name == "test.com"
        assert copy_builder._domain_id == "domain-123"
        
        # Modify copy and verify original unchanged
        copy_builder.page(2).limit(50).unverified_only().domain_id("domain-456")
        
        assert original._page == 1  # Original unchanged
        assert original._limit == 25  # Original unchanged
        assert original._verified is True  # Original unchanged
        assert original._domain_id == "domain-123"  # Original unchanged
        assert copy_builder._page == 2  # Copy changed
        assert copy_builder._limit == 50  # Copy changed
        assert copy_builder._verified is False  # Copy changed
        assert copy_builder._domain_id == "domain-456"  # Copy changed


class TestDomainsBuilderPagination:
    """Test pagination methods."""
    
    def test_page_method(self):
        """Test page method."""
        builder = DomainsBuilder()
        
        # Test valid pages
        builder.page(1)
        assert builder._page == 1
        
        builder.page(100)
        assert builder._page == 100
        
        # Test invalid pages raise validation errors
        with pytest.raises(MailerSendValidationError, match="Page must be greater than 0"):
            builder.page(0)
        
        with pytest.raises(MailerSendValidationError, match="Page must be greater than 0"):
            builder.page(-1)
    
    def test_limit_method(self):
        """Test limit method."""
        builder = DomainsBuilder()
        
        # Test valid limits
        builder.limit(10)  # Min
        assert builder._limit == 10
        
        builder.limit(100)  # Max  
        assert builder._limit == 100
        
        builder.limit(25)  # Middle
        assert builder._limit == 25
        
        # Test invalid limits raise validation errors
        with pytest.raises(MailerSendValidationError, match="Limit must be between 10 and 100"):
            builder.limit(5)
        
        with pytest.raises(MailerSendValidationError, match="Limit must be between 10 and 100"):
            builder.limit(150)


class TestDomainsBuilderFiltering:
    """Test filtering methods."""
    
    def test_verified_method(self):
        """Test verified method sets verified filter."""
        builder = DomainsBuilder()
        
        builder.verified(True)
        assert builder._verified is True
        
        builder.verified(False)
        assert builder._verified is False
    
    def test_verified_only_method(self):
        """Test verified_only method sets verified filter to True."""
        builder = DomainsBuilder().verified_only()
        assert builder._verified is True
    
    def test_unverified_only_method(self):
        """Test unverified_only method sets verified filter to False."""
        builder = DomainsBuilder().unverified_only()
        assert builder._verified is False


class TestDomainsBuilderDomainCreation:
    """Test domain creation methods."""
    
    def test_domain_name_method(self):
        """Test domain_name method."""
        builder = DomainsBuilder()
        
        builder.domain_name("example.com")
        assert builder._name == "example.com"
        
        builder.domain_name("sub.domain.org")
        assert builder._name == "sub.domain.org"
    
    def test_return_path_subdomain_method(self):
        """Test return_path_subdomain method."""
        builder = DomainsBuilder()
        
        builder.return_path_subdomain("mail")
        assert builder._return_path_subdomain == "mail"
        
        builder.return_path_subdomain("email123")
        assert builder._return_path_subdomain == "email123"
    
    def test_custom_tracking_subdomain_method(self):
        """Test custom_tracking_subdomain method.""" 
        builder = DomainsBuilder()
        
        builder.custom_tracking_subdomain("track")
        assert builder._custom_tracking_subdomain == "track"
        
        builder.custom_tracking_subdomain("links123")
        assert builder._custom_tracking_subdomain == "links123"
    
    def test_inbound_routing_subdomain_method(self):
        """Test inbound_routing_subdomain method."""
        builder = DomainsBuilder()
        
        builder.inbound_routing_subdomain("inbox")
        assert builder._inbound_routing_subdomain == "inbox"
        
        builder.inbound_routing_subdomain("inbound123")
        assert builder._inbound_routing_subdomain == "inbound123"


class TestDomainsBuilderDomainDeletion:
    """Test domain deletion methods."""
    
    def test_domain_id_method(self):
        """Test domain_id method."""
        builder = DomainsBuilder()
        
        builder.domain_id("domain-123")
        assert builder._domain_id == "domain-123"
        
        builder.domain_id("abc-456-def")
        assert builder._domain_id == "abc-456-def"


class TestDomainsBuilderSettings:
    """Test domain settings methods."""
    
    def test_individual_tracking_settings(self):
        """Test individual tracking setting methods."""
        builder = DomainsBuilder()
        
        # Test track_opens
        builder.track_opens(True)
        assert builder._track_opens is True
        
        builder.track_opens(False)
        assert builder._track_opens is False
        
        # Test track_clicks
        builder.track_clicks(True)
        assert builder._track_clicks is True
        
        # Test track_unsubscribe
        builder.track_unsubscribe(False)
        assert builder._track_unsubscribe is False
        
        # Test track_content
        builder.track_content(True)
        assert builder._track_content is True
    
    def test_sending_settings(self):
        """Test sending-related settings."""
        builder = DomainsBuilder()
        
        # Test send paused
        builder.send_paused(True)
        assert builder._send_paused is True
        
        # Test precedence bulk
        builder.precedence_bulk(False)
        assert builder._precedence_bulk is False
        
        # Test ignore duplicated recipients
        builder.ignore_duplicated_recipients(True)
        assert builder._ignore_duplicated_recipients is True
    
    def test_convenience_tracking_methods(self):
        """Test convenience methods for tracking settings."""
        builder = DomainsBuilder()
        
        # Test enable_all_tracking
        builder.enable_all_tracking()
        
        assert builder._track_opens is True
        assert builder._track_clicks is True
        assert builder._track_unsubscribe is True
        assert builder._track_content is True
        
        # Reset and test disable_all_tracking
        builder.reset()
        builder.disable_all_tracking()
        
        assert builder._track_opens is False
        assert builder._track_clicks is False
        assert builder._track_unsubscribe is False
        assert builder._track_content is False
    
    def test_convenience_sending_methods(self):
        """Test convenience methods for sending settings."""
        builder = DomainsBuilder()
        
        # Test pause_sending
        builder.pause_sending()
        assert builder._send_paused is True
        
        # Test resume_sending
        builder.resume_sending()
        assert builder._send_paused is False


class TestDomainsBuilderBuildMethods:
    """Test build methods that create request models."""
    
    def test_build_list_request_basic(self):
        """Test building basic list request."""
        builder = DomainsBuilder()
        request = builder.build_list_request()
        
        # Should create request with defaults
        assert isinstance(request, DomainListRequest)
        assert request.page is None
        assert request.limit is None  # Builder passes None which overrides model default
        assert request.verified is None
    
    def test_build_list_request_complete(self):
        """Test building complete list request."""
        builder = DomainsBuilder()
        builder.page(2).limit(50).verified(True)
        
        request = builder.build_list_request()
        
        assert isinstance(request, DomainListRequest)
        assert request.page == 2
        assert request.limit == 50
        assert request.verified is True
    
    def test_build_create_request_minimal(self):
        """Test building minimal create request."""
        builder = DomainsBuilder()
        builder.domain_name("example.com")
        
        request = builder.build_create_request()
        
        assert isinstance(request, DomainCreateRequest)
        assert request.name == "example.com"
        assert request.return_path_subdomain is None
        assert request.custom_tracking_subdomain is None
        assert request.inbound_routing_subdomain is None
    
    def test_build_create_request_complete(self):
        """Test building complete create request."""
        builder = DomainsBuilder()
        builder.domain_name("mydomain.com") \
            .return_path_subdomain("mail") \
            .custom_tracking_subdomain("track") \
            .inbound_routing_subdomain("inbox")
        
        request = builder.build_create_request()
        
        assert isinstance(request, DomainCreateRequest)
        assert request.name == "mydomain.com"
        assert request.return_path_subdomain == "mail"
        assert request.custom_tracking_subdomain == "track"
        assert request.inbound_routing_subdomain == "inbox"
    
    def test_build_create_request_missing_domain(self):
        """Test building create request without domain name raises error."""
        builder = DomainsBuilder()
        
        with pytest.raises(MailerSendValidationError, match="Domain name is required"):
            builder.build_create_request()
    
    def test_build_delete_request_basic(self):
        """Test building basic delete request."""
        builder = DomainsBuilder()
        builder.domain_id("domain-123")
        
        request = builder.build_delete_request()
        
        assert isinstance(request, DomainDeleteRequest)
        assert request.domain_id == "domain-123"
    
    def test_build_delete_request_missing_domain_id(self):
        """Test building delete request without domain ID raises error."""
        builder = DomainsBuilder()
        
        with pytest.raises(MailerSendValidationError, match="Domain ID is required"):
            builder.build_delete_request()
    
    def test_build_update_settings_request_empty(self):
        """Test building settings request with no updates."""
        builder = DomainsBuilder()
        builder.domain_id("test-domain-id")
        
        request = builder.build_update_settings_request()
        
        assert isinstance(request, DomainUpdateSettingsRequest)
        assert request.domain_id == "test-domain-id"
        assert request.send_paused is None
        assert request.track_clicks is None
        assert request.track_opens is None
    
    def test_build_update_settings_request_partial(self):
        """Test building settings request with partial updates."""
        builder = DomainsBuilder()
        builder.domain_id("test-domain-id").track_opens(True).send_paused(False)
        
        request = builder.build_update_settings_request()
        
        assert isinstance(request, DomainUpdateSettingsRequest)
        assert request.domain_id == "test-domain-id"
        assert request.track_opens is True
        assert request.send_paused is False
        assert request.track_clicks is None  # Not set
    
    def test_build_update_settings_request_complete(self):
        """Test building complete settings request."""
        builder = DomainsBuilder()
        builder.domain_id("test-domain-id") \
            .track_opens(True) \
            .track_clicks(False) \
            .track_content(True) \
            .send_paused(False) \
            .custom_tracking_enabled(True) \
            .precedence_bulk(True) \
            .ignore_duplicated_recipients(False)
        
        request = builder.build_update_settings_request()
        
        assert isinstance(request, DomainUpdateSettingsRequest)
        assert request.domain_id == "test-domain-id"
        assert request.track_opens is True
        assert request.track_clicks is False
        assert request.track_content is True
        assert request.send_paused is False
        assert request.custom_tracking_enabled is True
        assert request.precedence_bulk is True
        assert request.ignore_duplicated_recipients is False
    
    def test_build_recipients_request_basic(self):
        """Test building basic recipients request."""
        builder = DomainsBuilder()
        builder.domain_id("test-domain-id")
        
        request = builder.build_recipients_request()
        
        assert isinstance(request, DomainRecipientsRequest)
        assert request.domain_id == "test-domain-id"
        assert request.page is None
        assert request.limit is None  # Builder passes None which overrides model default

    def test_build_recipients_request_with_pagination(self):
        """Test building recipients request with pagination."""
        builder = DomainsBuilder()
        builder.domain_id("test-domain-id").page(3).limit(75)
        
        request = builder.build_recipients_request()
        
        assert isinstance(request, DomainRecipientsRequest)
        assert request.domain_id == "test-domain-id"
        assert request.page == 3
        assert request.limit == 75

    def test_build_get_request_basic(self):
        """Test building basic get request."""
        builder = DomainsBuilder()
        builder.domain_id("test-domain-id")
        
        request = builder.build_get_request()
        
        assert isinstance(request, DomainGetRequest)
        assert request.domain_id == "test-domain-id"

    def test_build_get_request_missing_domain_id(self):
        """Test building get request without domain ID."""
        builder = DomainsBuilder()
        
        with pytest.raises(MailerSendValidationError, match="Domain ID is required for getting domain"):
            builder.build_get_request()

    def test_build_dns_records_request_basic(self):
        """Test building basic DNS records request."""
        builder = DomainsBuilder()
        builder.domain_id("test-domain-id")
        
        request = builder.build_dns_records_request()
        
        assert isinstance(request, DomainDnsRecordsRequest)
        assert request.domain_id == "test-domain-id"

    def test_build_dns_records_request_missing_domain_id(self):
        """Test building DNS records request without domain ID."""
        builder = DomainsBuilder()
        
        with pytest.raises(MailerSendValidationError, match="Domain ID is required for getting DNS records"):
            builder.build_dns_records_request()

    def test_build_verification_request_basic(self):
        """Test building basic verification request."""
        builder = DomainsBuilder()
        builder.domain_id("test-domain-id")
        
        request = builder.build_verification_request()
        
        assert isinstance(request, DomainVerificationRequest)
        assert request.domain_id == "test-domain-id"

    def test_build_verification_request_missing_domain_id(self):
        """Test building verification request without domain ID."""
        builder = DomainsBuilder()
        
        with pytest.raises(MailerSendValidationError, match="Domain ID is required for getting verification status"):
            builder.build_verification_request()

    def test_build_update_settings_request_missing_domain_id(self):
        """Test building update settings request without domain ID."""
        builder = DomainsBuilder()
        
        with pytest.raises(MailerSendValidationError, match="Domain ID is required for updating settings"):
            builder.build_update_settings_request()

    def test_build_recipients_request_missing_domain_id(self):
        """Test building recipients request without domain ID."""
        builder = DomainsBuilder()
        
        with pytest.raises(MailerSendValidationError, match="Domain ID is required for getting recipients"):
            builder.build_recipients_request()


class TestDomainsBuilderComplexScenarios:
    """Test complex builder usage scenarios."""
    
    def test_chained_method_calls(self):
        """Test complex method chaining."""
        builder = DomainsBuilder()
        
        # Build a complex configuration in one chain
        result = (builder
                 .page(1)
                 .limit(50)
                 .verified(True)
                 .domain_name("example.com")
                 .return_path_subdomain("mail")
                 .custom_tracking_subdomain("track")
                 .track_opens(True)
                 .track_clicks(False)
                 .enable_all_tracking()  # Should override previous settings
                 .send_paused(False))
        
        # Verify all settings applied correctly
        assert result._page == 1
        assert result._limit == 50
        assert result._verified is True
        assert result._name == "example.com"
        assert result._return_path_subdomain == "mail"
        assert result._custom_tracking_subdomain == "track"
        assert result._track_opens is True  # From enable_all_tracking
        assert result._track_clicks is True  # enable_all_tracking overrode False
        assert result._send_paused is False
    
    def test_builder_reuse_with_reset(self):
        """Test reusing builder with reset between operations."""
        builder = DomainsBuilder()
        
        # First configuration
        builder.page(1).limit(25).verified(True).domain_name("first.com")
        first_list = builder.build_list_request()
        first_create = builder.build_create_request()
        
        assert first_list.page == 1
        assert first_list.verified is True
        assert first_create.name == "first.com"
        
        # Reset and second configuration
        builder.reset()
        builder.page(2).limit(50).unverified_only().domain_name("second.com")
        second_list = builder.build_list_request()
        second_create = builder.build_create_request()
        
        assert second_list.page == 2
        assert second_list.verified is False
        assert second_create.name == "second.com"
        
        # Verify first requests unchanged
        assert first_list.page == 1
        assert first_list.verified is True
        assert first_create.name == "first.com" 