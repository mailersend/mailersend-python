import pytest

from mailersend.builders.schedules import SchedulesBuilder
from mailersend.models.schedules import SchedulesListRequest, ScheduleGetRequest, ScheduleDeleteRequest
from mailersend.exceptions import ValidationError


class TestSchedulesBuilder:
    """Test SchedulesBuilder class."""
    
    def test_initialization(self):
        """Test builder initialization."""
        builder = SchedulesBuilder()
        assert builder is not None
        assert builder._domain_id is None
        assert builder._status is None
        assert builder._page is None
        assert builder._limit is None
        assert builder._message_id is None
    
    def test_domain_id_method(self):
        """Test domain_id method."""
        builder = SchedulesBuilder()
        result = builder.domain_id("test-domain")
        assert result is builder  # Test fluent interface
        assert builder._domain_id == "test-domain"
    
    def test_domain_id_validation_empty(self):
        """Test domain_id validation with empty string."""
        builder = SchedulesBuilder()
        with pytest.raises(ValidationError) as exc_info:
            builder.domain_id("")
        assert "Domain ID cannot be empty" in str(exc_info.value)
    
    def test_domain_id_validation_whitespace(self):
        """Test domain_id validation with whitespace."""
        builder = SchedulesBuilder()
        with pytest.raises(ValidationError) as exc_info:
            builder.domain_id("   ")
        assert "Domain ID cannot be empty" in str(exc_info.value)
    
    def test_domain_id_trimming(self):
        """Test domain_id trimming."""
        builder = SchedulesBuilder()
        builder.domain_id("  test-domain  ")
        assert builder._domain_id == "test-domain"
    
    def test_status_method(self):
        """Test status method."""
        builder = SchedulesBuilder()
        result = builder.status("scheduled")
        assert result is builder  # Test fluent interface
        assert builder._status == "scheduled"
    
    def test_status_convenience_methods(self):
        """Test status convenience methods."""
        builder = SchedulesBuilder()
        
        # Test scheduled_only
        builder.scheduled_only()
        assert builder._status == "scheduled"
        
        # Test sent_only
        builder.sent_only()
        assert builder._status == "sent"
        
        # Test error_only
        builder.error_only()
        assert builder._status == "error"
    
    def test_page_method(self):
        """Test page method."""
        builder = SchedulesBuilder()
        result = builder.page(2)
        assert result is builder  # Test fluent interface
        assert builder._page == 2
    
    def test_page_validation_zero(self):
        """Test page validation with zero."""
        builder = SchedulesBuilder()
        with pytest.raises(ValidationError) as exc_info:
            builder.page(0)
        assert "Page must be greater than 0" in str(exc_info.value)
    
    def test_page_validation_negative(self):
        """Test page validation with negative number."""
        builder = SchedulesBuilder()
        with pytest.raises(ValidationError) as exc_info:
            builder.page(-1)
        assert "Page must be greater than 0" in str(exc_info.value)
    
    def test_limit_method(self):
        """Test limit method."""
        builder = SchedulesBuilder()
        result = builder.limit(50)
        assert result is builder  # Test fluent interface
        assert builder._limit == 50
    
    def test_limit_validation_min(self):
        """Test limit validation - minimum value."""
        builder = SchedulesBuilder()
        with pytest.raises(ValidationError) as exc_info:
            builder.limit(5)
        assert "Limit must be between 10 and 100" in str(exc_info.value)
    
    def test_limit_validation_max(self):
        """Test limit validation - maximum value."""
        builder = SchedulesBuilder()
        with pytest.raises(ValidationError) as exc_info:
            builder.limit(150)
        assert "Limit must be between 10 and 100" in str(exc_info.value)
    
    def test_limit_boundaries(self):
        """Test limit boundaries."""
        builder = SchedulesBuilder()
        
        # Test minimum valid value
        builder.limit(10)
        assert builder._limit == 10
        
        # Test maximum valid value
        builder.limit(100)
        assert builder._limit == 100
    
    def test_message_id_method(self):
        """Test message_id method."""
        builder = SchedulesBuilder()
        result = builder.message_id("61e01f471053b349a5478a52")
        assert result is builder  # Test fluent interface
        assert builder._message_id == "61e01f471053b349a5478a52"
    
    def test_message_id_validation_empty(self):
        """Test message_id validation with empty string."""
        builder = SchedulesBuilder()
        with pytest.raises(ValidationError) as exc_info:
            builder.message_id("")
        assert "Message ID cannot be empty" in str(exc_info.value)
    
    def test_message_id_validation_whitespace(self):
        """Test message_id validation with whitespace."""
        builder = SchedulesBuilder()
        with pytest.raises(ValidationError) as exc_info:
            builder.message_id("   ")
        assert "Message ID cannot be empty" in str(exc_info.value)
    
    def test_message_id_trimming(self):
        """Test message_id trimming."""
        builder = SchedulesBuilder()
        builder.message_id("  61e01f471053b349a5478a52  ")
        assert builder._message_id == "61e01f471053b349a5478a52"
    
    def test_build_list_request_default(self):
        """Test building list request with default values."""
        builder = SchedulesBuilder()
        request = builder.build_list_request()
        
        assert isinstance(request, SchedulesListRequest)
        assert request.domain_id is None
        assert request.status is None
        assert request.page is None
        assert request.limit == 25  # Default value
    
    def test_build_list_request_with_parameters(self):
        """Test building list request with custom parameters."""
        builder = SchedulesBuilder()
        request = (builder
                   .domain_id("test-domain")
                   .status("scheduled")
                   .page(2)
                   .limit(50)
                   .build_list_request())
        
        assert isinstance(request, SchedulesListRequest)
        assert request.domain_id == "test-domain"
        assert request.status == "scheduled"
        assert request.page == 2
        assert request.limit == 50
    
    def test_build_get_request(self):
        """Test building get request."""
        builder = SchedulesBuilder()
        request = builder.message_id("61e01f471053b349a5478a52").build_get_request()
        
        assert isinstance(request, ScheduleGetRequest)
        assert request.message_id == "61e01f471053b349a5478a52"
    
    def test_build_get_request_without_message_id(self):
        """Test building get request without message ID."""
        builder = SchedulesBuilder()
        with pytest.raises(ValidationError) as exc_info:
            builder.build_get_request()
        assert "Message ID must be set to build get request" in str(exc_info.value)
    
    def test_build_delete_request(self):
        """Test building delete request."""
        builder = SchedulesBuilder()
        request = builder.message_id("61e01f471053b349a5478a52").build_delete_request()
        
        assert isinstance(request, ScheduleDeleteRequest)
        assert request.message_id == "61e01f471053b349a5478a52"
    
    def test_build_delete_request_without_message_id(self):
        """Test building delete request without message ID."""
        builder = SchedulesBuilder()
        with pytest.raises(ValidationError) as exc_info:
            builder.build_delete_request()
        assert "Message ID must be set to build delete request" in str(exc_info.value)
    
    def test_reset_method(self):
        """Test reset method."""
        builder = SchedulesBuilder()
        builder.domain_id("test").status("scheduled").page(2).limit(50).message_id("test-id")
        
        result = builder.reset()
        assert result is builder  # Test fluent interface
        assert builder._domain_id is None
        assert builder._status is None
        assert builder._page is None
        assert builder._limit is None
        assert builder._message_id is None
    
    def test_copy_method(self):
        """Test copy method."""
        builder = SchedulesBuilder()
        builder.domain_id("test-domain").status("scheduled").page(3).limit(75).message_id("test-message-id")
        
        copied_builder = builder.copy()
        
        # Verify it's a different instance
        assert copied_builder is not builder
        
        # Verify same configuration
        assert copied_builder._domain_id == "test-domain"
        assert copied_builder._status == "scheduled"
        assert copied_builder._page == 3
        assert copied_builder._limit == 75
        assert copied_builder._message_id == "test-message-id"
        
        # Verify modifications to copy don't affect original
        copied_builder.page(5)
        assert builder._page == 3
        assert copied_builder._page == 5
    
    def test_method_chaining(self):
        """Test method chaining with multiple calls."""
        builder = SchedulesBuilder()
        result = (builder
                  .domain_id("test")
                  .status("scheduled")
                  .page(1)
                  .limit(25)
                  .message_id("test-id")
                  .reset()
                  .page(2))
        
        assert result is builder  # All methods return self
        assert builder._page == 2
        assert builder._domain_id is None  # Reset cleared this
        assert builder._status is None  # Reset cleared this
        assert builder._limit is None  # Reset cleared this
        assert builder._message_id is None  # Reset cleared this
    
    def test_fluent_interface_with_build(self):
        """Test complete fluent interface workflow."""
        builder = SchedulesBuilder()
        
        # Test list request workflow
        list_request = (builder
                        .domain_id("test-domain")
                        .scheduled_only()
                        .page(1)
                        .limit(10)
                        .build_list_request())
        assert list_request.domain_id == "test-domain"
        assert list_request.status == "scheduled"
        assert list_request.page == 1
        assert list_request.limit == 10
        
        # Test get request workflow (after reset)
        get_request = builder.reset().message_id("abc123").build_get_request()
        assert get_request.message_id == "abc123"
        
        # Test delete request workflow (reusing message_id)
        delete_request = builder.build_delete_request()
        assert delete_request.message_id == "abc123"
    
    def test_status_values_fluent_methods(self):
        """Test fluent interface for all status values."""
        builder = SchedulesBuilder()
        
        # Test each status convenience method returns correct status
        request1 = builder.scheduled_only().build_list_request()
        assert request1.status == "scheduled"
        
        request2 = builder.sent_only().build_list_request()
        assert request2.status == "sent"
        
        request3 = builder.error_only().build_list_request()
        assert request3.status == "error" 