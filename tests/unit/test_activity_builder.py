import pytest
from datetime import datetime

from mailersend.builders.activity import ActivityBuilder, SingleActivityBuilder
from mailersend.models.activity import ActivityRequest, SingleActivityRequest


class TestActivityBuilder:
    """Test cases for ActivityBuilder."""
    
    def test_basic_builder_creation(self):
        """Test basic builder instantiation."""
        builder = ActivityBuilder()
        assert builder is not None
    
    def test_domain_id_setting(self):
        """Test setting domain ID."""
        builder = ActivityBuilder()
        result = builder.domain_id("test-domain")
        
        assert result is builder  # Should return self for chaining
        request = builder.date_from(1672574400).date_to(1672660800).build()
        assert request.domain_id == "test-domain"
    
    def test_page_setting(self):
        """Test setting page number."""
        builder = ActivityBuilder()
        result = builder.page(2)
        
        assert result is builder
        request = builder.domain_id("test").date_from(1672574400).date_to(1672660800).build()
        assert request.query_params.page == 2
    
    def test_limit_setting(self):
        """Test setting limit."""
        builder = ActivityBuilder()
        result = builder.limit(50)
        
        assert result is builder
        request = builder.domain_id("test").date_from(1672574400).date_to(1672660800).build()
        assert request.query_params.limit == 50
    
    def test_date_from_datetime(self):
        """Test setting date_from with datetime."""
        builder = ActivityBuilder()
        test_date = datetime(2023, 1, 1, 12, 0, 0)
        result = builder.date_from(test_date)
        
        assert result is builder
        request = builder.domain_id("test").date_to(1672660800).build()
        assert request.query_params.date_from == int(test_date.timestamp())
    
    def test_date_from_timestamp(self):
        """Test setting date_from with timestamp."""
        builder = ActivityBuilder()
        timestamp = 1672574400  # 2023-01-01 12:00:00 UTC
        result = builder.date_from(timestamp)
        
        assert result is builder
        request = builder.domain_id("test").date_to(1672660800).build()
        assert request.query_params.date_from == timestamp
    
    def test_date_to_datetime(self):
        """Test setting date_to with datetime."""
        builder = ActivityBuilder()
        test_date = datetime(2023, 1, 2, 12, 0, 0)
        result = builder.date_to(test_date)
        
        assert result is builder
        request = builder.domain_id("test").date_from(1672574400).build()
        assert request.query_params.date_to == int(test_date.timestamp())
    
    def test_date_to_timestamp(self):
        """Test setting date_to with timestamp."""
        builder = ActivityBuilder()
        timestamp = 1672660800  # 2023-01-02 12:00:00 UTC
        result = builder.date_to(timestamp)
        
        assert result is builder
        request = builder.domain_id("test").date_from(1672574400).build()
        assert request.query_params.date_to == timestamp
    
    def test_single_event(self):
        """Test adding a single event."""
        builder = ActivityBuilder()
        result = builder.event("sent")
        
        assert result is builder
        request = builder.domain_id("test").date_from(1672574400).date_to(1672660800).build()
        assert request.query_params.event == ["sent"]
    
    def test_multiple_events_via_events_method(self):
        """Test setting multiple events via events method."""
        builder = ActivityBuilder()
        events = ["sent", "delivered", "opened"]
        result = builder.events(events)
        
        assert result is builder
        request = builder.domain_id("test").date_from(1672574400).date_to(1672660800).build()
        assert request.query_params.event == events
    
    def test_multiple_events_via_event_method(self):
        """Test adding multiple events via repeated event calls."""
        builder = ActivityBuilder()
        builder.event("sent").event("delivered").event("opened")
        
        request = builder.domain_id("test").date_from(1672574400).date_to(1672660800).build()
        assert request.query_params.event == ["sent", "delivered", "opened"]
    
    def test_duplicate_events_ignored(self):
        """Test that duplicate events are ignored."""
        builder = ActivityBuilder()
        builder.event("sent").event("sent").event("delivered")
        
        request = builder.domain_id("test").date_from(1672574400).date_to(1672660800).build()
        assert request.query_params.event == ["sent", "delivered"]
    
    def test_method_chaining(self):
        """Test method chaining works correctly."""
        builder = ActivityBuilder()
        result = (builder
                 .domain_id("test-domain")
                 .page(2)
                 .limit(50)
                 .date_from(1672574400)
                 .date_to(1672660800)
                 .event("sent")
                 .event("delivered"))
        
        assert result is builder
        request = builder.build()
        assert request.domain_id == "test-domain"
        assert request.query_params.page == 2
        assert request.query_params.limit == 50
        assert request.query_params.date_from == 1672574400
        assert request.query_params.date_to == 1672660800
        assert request.query_params.event == ["sent", "delivered"]
    
    def test_copy_builder(self):
        """Test copying a builder."""
        original = ActivityBuilder()
        original.domain_id("test-domain").page(2).event("sent").date_from(1672574400).date_to(1672660800)
        
        copy = original.copy()
        
        # Verify copy has same values
        copy_request = copy.build()
        original_request = original.build()
        
        assert copy_request.domain_id == original_request.domain_id
        assert copy_request.query_params.page == original_request.query_params.page
        assert copy_request.query_params.event == original_request.query_params.event
        
        # Verify they are independent
        copy.domain_id("different-domain")
        assert original.build().domain_id == "test-domain"
        assert copy.build().domain_id == "different-domain"
    
    def test_reset_builder(self):
        """Test resetting a builder."""
        builder = ActivityBuilder()
        builder.domain_id("test-domain").page(2).event("sent").date_from(1672574400).date_to(1672660800)
        
        # Verify builder has values
        request_before = builder.build()
        assert request_before.domain_id == "test-domain"
        assert request_before.query_params.page == 2
        assert request_before.query_params.event == ["sent"]
        
        # Reset and verify values are cleared
        result = builder.reset()
        assert result is builder
        
        # After reset, we can't build without required fields, so just check internal state
        assert builder._domain_id is None
        assert builder._page is None
        assert builder._event == []
    
    def test_empty_events_list_becomes_none(self):
        """Test that empty events list becomes None in build."""
        builder = ActivityBuilder()
        request = builder.domain_id("test").date_from(1672574400).date_to(1672660800).build()
        assert request.query_params.event is None
    
    def test_build_returns_activity_request(self):
        """Test that build returns ActivityRequest instance."""
        builder = ActivityBuilder()
        request = builder.domain_id("test").date_from(1672574400).date_to(1672660800).build()
        assert isinstance(request, ActivityRequest)


class TestSingleActivityBuilder:
    """Test cases for SingleActivityBuilder."""
    
    def test_basic_builder_creation(self):
        """Test basic builder instantiation."""
        builder = SingleActivityBuilder()
        assert builder is not None
    
    def test_activity_id_setting(self):
        """Test setting activity ID."""
        builder = SingleActivityBuilder()
        result = builder.activity_id("5ee0b166b251345e407c9207")
        
        assert result is builder  # Should return self for chaining
        request = builder.build()
        assert request.activity_id == "5ee0b166b251345e407c9207"
    
    def test_method_chaining(self):
        """Test method chaining works correctly."""
        builder = SingleActivityBuilder()
        result = builder.activity_id("5ee0b166b251345e407c9207")
        
        assert result is builder
        request = builder.build()
        assert request.activity_id == "5ee0b166b251345e407c9207"
    
    def test_copy_builder(self):
        """Test copying a builder."""
        original = SingleActivityBuilder()
        original.activity_id("5ee0b166b251345e407c9207")
        
        copy = original.copy()
        
        # Verify copy has same values
        copy_request = copy.build()
        original_request = original.build()
        
        assert copy_request.activity_id == original_request.activity_id
        
        # Verify they are independent
        copy.activity_id("different-id")
        assert original.build().activity_id == "5ee0b166b251345e407c9207"
        assert copy.build().activity_id == "different-id"
    
    def test_reset_builder(self):
        """Test resetting a builder."""
        builder = SingleActivityBuilder()
        builder.activity_id("5ee0b166b251345e407c9207")
        
        # Verify builder has values
        request_before = builder.build()
        assert request_before.activity_id == "5ee0b166b251345e407c9207"
        
        # Reset and verify values are cleared
        result = builder.reset()
        assert result is builder
        
        # After reset, we can't build without required fields, so just check internal state
        assert builder._activity_id is None
    
    def test_build_without_activity_id_raises_error(self):
        """Test that building without activity_id raises ValueError."""
        builder = SingleActivityBuilder()
        
        with pytest.raises(ValueError) as exc_info:
            builder.build()
        
        assert "activity_id is required" in str(exc_info.value)
    
    def test_build_returns_single_activity_request(self):
        """Test that build returns SingleActivityRequest instance."""
        builder = SingleActivityBuilder()
        request = builder.activity_id("5ee0b166b251345e407c9207").build()
        assert isinstance(request, SingleActivityRequest) 