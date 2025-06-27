import pytest
from copy import deepcopy

from mailersend.builders.identities import IdentityBuilder
from mailersend.exceptions import ValidationError as MailerSendValidationError
from mailersend.models.identities import (
    IdentityListRequest,
    IdentityCreateRequest,
    IdentityGetRequest,
    IdentityGetByEmailRequest,
    IdentityUpdateRequest,
    IdentityUpdateByEmailRequest,
    IdentityDeleteRequest,
    IdentityDeleteByEmailRequest
)


class TestIdentityBuilder:
    """Test IdentityBuilder class."""

    def test_initialization(self):
        """Test builder initialization."""
        builder = IdentityBuilder()
        assert builder._domain_id is None
        assert builder._page is None
        assert builder._limit is None
        assert builder._identity_id is None
        assert builder._email is None
        assert builder._name is None
        assert builder._reply_to_email is None
        assert builder._reply_to_name is None
        assert builder._add_note is None
        assert builder._personal_note is None

    def test_reset(self):
        """Test builder reset functionality."""
        builder = IdentityBuilder()
        builder.domain_id("domain123").name("John Doe").email("john@example.com")
        
        # Verify values are set
        assert builder._domain_id == "domain123"
        assert builder._name == "John Doe"
        assert builder._email == "john@example.com"
        
        # Reset builder
        result = builder.reset()
        
        # Verify reset worked and returns self
        assert result is builder
        assert builder._domain_id is None
        assert builder._name is None
        assert builder._email is None

    def test_copy(self):
        """Test builder copy functionality."""
        builder = IdentityBuilder()
        builder.domain_id("domain123").name("John Doe").email("john@example.com")
        builder.reply_to_email("reply@example.com").add_note(True)
        
        # Create copy
        copy_builder = builder.copy()
        
        # Verify copy has same values
        assert copy_builder._domain_id == "domain123"
        assert copy_builder._name == "John Doe"
        assert copy_builder._email == "john@example.com"
        assert copy_builder._reply_to_email == "reply@example.com"
        assert copy_builder._add_note is True
        
        # Verify they are different objects
        assert copy_builder is not builder
        
        # Verify modifying copy doesn't affect original
        copy_builder.name("Jane Doe")
        assert builder._name == "John Doe"
        assert copy_builder._name == "Jane Doe"

    def test_pagination_methods(self):
        """Test pagination methods."""
        builder = IdentityBuilder()
        
        # Test page method
        result = builder.page(2)
        assert result is builder  # Fluent interface
        assert builder._page == 2
        
        # Test limit method
        result = builder.limit(50)
        assert result is builder  # Fluent interface
        assert builder._limit == 50

    def test_filtering_methods(self):
        """Test filtering methods."""
        builder = IdentityBuilder()
        
        # Test domain_id method
        result = builder.domain_id("domain123")
        assert result is builder  # Fluent interface
        assert builder._domain_id == "domain123"

    def test_identity_identification_methods(self):
        """Test identity identification methods."""
        builder = IdentityBuilder()
        
        # Test identity_id method
        result = builder.identity_id("identity123")
        assert result is builder  # Fluent interface
        assert builder._identity_id == "identity123"
        
        # Test email method
        result = builder.email("john@example.com")
        assert result is builder  # Fluent interface
        assert builder._email == "john@example.com"

    def test_identity_data_methods(self):
        """Test identity data methods."""
        builder = IdentityBuilder()
        
        # Test name method
        result = builder.name("John Doe")
        assert result is builder  # Fluent interface
        assert builder._name == "John Doe"
        
        # Test reply_to_email method
        result = builder.reply_to_email("reply@example.com")
        assert result is builder  # Fluent interface
        assert builder._reply_to_email == "reply@example.com"
        
        # Test reply_to_name method
        result = builder.reply_to_name("Reply Name")
        assert result is builder  # Fluent interface
        assert builder._reply_to_name == "Reply Name"
        
        # Test add_note method
        result = builder.add_note(True)
        assert result is builder  # Fluent interface
        assert builder._add_note is True
        
        # Test personal_note method
        result = builder.personal_note("Personal note content")
        assert result is builder  # Fluent interface
        assert builder._personal_note == "Personal note content"

    def test_convenience_methods(self):
        """Test convenience methods."""
        builder = IdentityBuilder()
        
        # Test enable_personal_note
        result = builder.enable_personal_note("Test note")
        assert result is builder  # Fluent interface
        assert builder._add_note is True
        assert builder._personal_note == "Test note"
        
        # Test disable_personal_note
        result = builder.disable_personal_note()
        assert result is builder  # Fluent interface
        assert builder._add_note is False
        assert builder._personal_note is None
        
        # Test with_reply_to with email only
        result = builder.with_reply_to("reply@example.com")
        assert result is builder  # Fluent interface
        assert builder._reply_to_email == "reply@example.com"
        assert builder._reply_to_name is None
        
        # Test with_reply_to with email and name
        result = builder.with_reply_to("reply2@example.com", "Reply Name")
        assert result is builder  # Fluent interface
        assert builder._reply_to_email == "reply2@example.com"
        assert builder._reply_to_name == "Reply Name"
        
        # Test clear_reply_to
        result = builder.clear_reply_to()
        assert result is builder  # Fluent interface
        assert builder._reply_to_email is None
        assert builder._reply_to_name is None

    def test_method_chaining(self):
        """Test fluent interface method chaining."""
        builder = IdentityBuilder()
        
        result = (builder
                 .domain_id("domain123")
                 .name("John Doe")
                 .email("john@example.com")
                 .reply_to_email("reply@example.com")
                 .reply_to_name("Reply Name")
                 .enable_personal_note("Test note")
                 .page(2)
                 .limit(50))
        
        assert result is builder  # Fluent interface
        assert builder._domain_id == "domain123"
        assert builder._name == "John Doe"
        assert builder._email == "john@example.com"
        assert builder._reply_to_email == "reply@example.com"
        assert builder._reply_to_name == "Reply Name"
        assert builder._add_note is True
        assert builder._personal_note == "Test note"
        assert builder._page == 2
        assert builder._limit == 50

    def test_build_list_request(self):
        """Test building list request."""
        builder = IdentityBuilder()
        
        # Test with no parameters
        request = builder.build_list_request()
        assert isinstance(request, IdentityListRequest)
        assert request.domain_id is None
        assert request.page is None
        assert request.limit is None  # Builder passes None, model will use default
        
        # Test with all parameters
        builder.domain_id("domain123").page(2).limit(50)
        request = builder.build_list_request()
        assert isinstance(request, IdentityListRequest)
        assert request.domain_id == "domain123"
        assert request.page == 2
        assert request.limit == 50

    def test_build_create_request(self):
        """Test building create request."""
        builder = IdentityBuilder()
        
        # Test with missing required fields
        with pytest.raises(MailerSendValidationError, match="Domain ID is required"):
            builder.build_create_request()
        
        with pytest.raises(MailerSendValidationError, match="Name is required"):
            builder.domain_id("domain123").build_create_request()
        
        with pytest.raises(MailerSendValidationError, match="Email is required"):
            builder.domain_id("domain123").name("John Doe").build_create_request()
        
        # Test with required fields only
        builder.domain_id("domain123").name("John Doe").email("john@example.com")
        request = builder.build_create_request()
        assert isinstance(request, IdentityCreateRequest)
        assert request.domain_id == "domain123"
        assert request.name == "John Doe"
        assert request.email == "john@example.com"
        assert request.reply_to_email is None
        assert request.reply_to_name is None
        assert request.add_note is None
        assert request.personal_note is None
        
        # Test with all fields
        builder.reply_to_email("reply@example.com").reply_to_name("Reply Name")
        builder.add_note(True).personal_note("Personal note")
        request = builder.build_create_request()
        assert isinstance(request, IdentityCreateRequest)
        assert request.domain_id == "domain123"
        assert request.name == "John Doe"
        assert request.email == "john@example.com"
        assert request.reply_to_email == "reply@example.com"
        assert request.reply_to_name == "Reply Name"
        assert request.add_note is True
        assert request.personal_note == "Personal note"

    def test_build_get_request(self):
        """Test building get request."""
        builder = IdentityBuilder()
        
        # Test with missing identity ID
        with pytest.raises(MailerSendValidationError, match="Identity ID is required"):
            builder.build_get_request()
        
        # Test with identity ID
        builder.identity_id("identity123")
        request = builder.build_get_request()
        assert isinstance(request, IdentityGetRequest)
        assert request.identity_id == "identity123"

    def test_build_get_by_email_request(self):
        """Test building get by email request."""
        builder = IdentityBuilder()
        
        # Test with missing email
        with pytest.raises(MailerSendValidationError, match="Email is required"):
            builder.build_get_by_email_request()
        
        # Test with email
        builder.email("john@example.com")
        request = builder.build_get_by_email_request()
        assert isinstance(request, IdentityGetByEmailRequest)
        assert request.email == "john@example.com"

    def test_build_update_request(self):
        """Test building update request."""
        builder = IdentityBuilder()
        
        # Test with missing identity ID
        with pytest.raises(MailerSendValidationError, match="Identity ID is required"):
            builder.build_update_request()
        
        # Test with identity ID only
        builder.identity_id("identity123")
        request = builder.build_update_request()
        assert isinstance(request, IdentityUpdateRequest)
        assert request.identity_id == "identity123"
        assert request.name is None
        assert request.reply_to_email is None
        assert request.reply_to_name is None
        assert request.add_note is None
        assert request.personal_note is None
        
        # Test with all update fields
        builder.name("Updated Name").reply_to_email("updated@example.com")
        builder.reply_to_name("Updated Reply").add_note(False).personal_note("Updated note")
        request = builder.build_update_request()
        assert isinstance(request, IdentityUpdateRequest)
        assert request.identity_id == "identity123"
        assert request.name == "Updated Name"
        assert request.reply_to_email == "updated@example.com"
        assert request.reply_to_name == "Updated Reply"
        assert request.add_note is False
        assert request.personal_note == "Updated note"

    def test_build_update_by_email_request(self):
        """Test building update by email request."""
        builder = IdentityBuilder()
        
        # Test with missing email
        with pytest.raises(MailerSendValidationError, match="Email is required"):
            builder.build_update_by_email_request()
        
        # Test with email only
        builder.email("john@example.com")
        request = builder.build_update_by_email_request()
        assert isinstance(request, IdentityUpdateByEmailRequest)
        assert request.email == "john@example.com"
        assert request.name is None
        assert request.reply_to_email is None
        assert request.reply_to_name is None
        assert request.add_note is None
        assert request.personal_note is None
        
        # Test with all update fields
        builder.name("Updated Name").reply_to_email("updated@example.com")
        builder.reply_to_name("Updated Reply").add_note(False).personal_note("Updated note")
        request = builder.build_update_by_email_request()
        assert isinstance(request, IdentityUpdateByEmailRequest)
        assert request.email == "john@example.com"
        assert request.name == "Updated Name"
        assert request.reply_to_email == "updated@example.com"
        assert request.reply_to_name == "Updated Reply"
        assert request.add_note is False
        assert request.personal_note == "Updated note"

    def test_build_delete_request(self):
        """Test building delete request."""
        builder = IdentityBuilder()
        
        # Test with missing identity ID
        with pytest.raises(MailerSendValidationError, match="Identity ID is required"):
            builder.build_delete_request()
        
        # Test with identity ID
        builder.identity_id("identity123")
        request = builder.build_delete_request()
        assert isinstance(request, IdentityDeleteRequest)
        assert request.identity_id == "identity123"

    def test_build_delete_by_email_request(self):
        """Test building delete by email request."""
        builder = IdentityBuilder()
        
        # Test with missing email
        with pytest.raises(MailerSendValidationError, match="Email is required"):
            builder.build_delete_by_email_request()
        
        # Test with email
        builder.email("john@example.com")
        request = builder.build_delete_by_email_request()
        assert isinstance(request, IdentityDeleteByEmailRequest)
        assert request.email == "john@example.com"

    def test_builder_state_independence(self):
        """Test that different build methods don't interfere with each other."""
        builder = IdentityBuilder()
        
        # Set up builder with mixed data
        builder.domain_id("domain123").identity_id("identity123").email("john@example.com")
        builder.name("John Doe").reply_to_email("reply@example.com")
        
        # Build different request types
        list_request = builder.build_list_request()
        get_request = builder.build_get_request()
        get_by_email_request = builder.build_get_by_email_request()
        create_request = builder.build_create_request()
        update_request = builder.build_update_request()
        update_by_email_request = builder.build_update_by_email_request()
        delete_request = builder.build_delete_request()
        delete_by_email_request = builder.build_delete_by_email_request()
        
        # Verify each request has appropriate fields
        assert list_request.domain_id == "domain123"
        assert get_request.identity_id == "identity123"
        assert get_by_email_request.email == "john@example.com"
        assert create_request.domain_id == "domain123"
        assert create_request.name == "John Doe"
        assert create_request.email == "john@example.com"
        assert update_request.identity_id == "identity123"
        assert update_request.name == "John Doe"
        assert update_by_email_request.email == "john@example.com"
        assert update_by_email_request.name == "John Doe"
        assert delete_request.identity_id == "identity123"
        assert delete_by_email_request.email == "john@example.com"

    def test_complex_workflow_scenarios(self):
        """Test complex workflow scenarios."""
        builder = IdentityBuilder()
        
        # Scenario 1: Create identity with personal note
        create_request = (builder
                         .domain_id("domain123")
                         .name("John Doe")
                         .email("john@example.com")
                         .with_reply_to("reply@example.com", "Reply Name")
                         .enable_personal_note("Welcome to our service!")
                         .build_create_request())
        
        assert create_request.domain_id == "domain123"
        assert create_request.name == "John Doe"
        assert create_request.email == "john@example.com"
        assert create_request.reply_to_email == "reply@example.com"
        assert create_request.reply_to_name == "Reply Name"
        assert create_request.add_note is True
        assert create_request.personal_note == "Welcome to our service!"
        
        # Scenario 2: Update identity to disable personal note
        update_request = (builder
                         .reset()
                         .identity_id("identity123")
                         .name("John Smith")
                         .disable_personal_note()
                         .clear_reply_to()
                         .build_update_request())
        
        assert update_request.identity_id == "identity123"
        assert update_request.name == "John Smith"
        assert update_request.add_note is False
        assert update_request.personal_note is None
        assert update_request.reply_to_email is None
        assert update_request.reply_to_name is None
        
        # Scenario 3: List identities with pagination
        list_request = (builder
                       .reset()
                       .domain_id("domain456")
                       .page(3)
                       .limit(25)
                       .build_list_request())
        
        assert list_request.domain_id == "domain456"
        assert list_request.page == 3
        assert list_request.limit == 25

    def test_edge_cases(self):
        """Test edge cases and boundary conditions."""
        builder = IdentityBuilder()
        
        # Test with empty strings (should be handled by model validation)
        builder.domain_id("domain123").name("John Doe").email("john@example.com")
        request = builder.build_create_request()
        # Should succeed since validation happens in model
        
        # Test with None values explicitly set
        builder.reply_to_email(None).reply_to_name(None)
        request = builder.build_create_request()
        assert request.reply_to_email is None
        assert request.reply_to_name is None
        
        # Test boolean values
        builder.add_note(False)
        request = builder.build_create_request()
        assert request.add_note is False
        
        builder.add_note(True)
        request = builder.build_create_request()
        assert request.add_note is True

    def test_builder_reuse(self):
        """Test builder can be reused for multiple operations."""
        builder = IdentityBuilder()
        
        # Build first request
        request1 = (builder
                   .domain_id("domain123")
                   .name("John Doe")
                   .email("john@example.com")
                   .build_create_request())
        
        # Modify and build second request
        request2 = (builder
                   .name("Jane Doe")
                   .email("jane@example.com")
                   .build_create_request())
        
        # Verify both requests
        assert request1.name == "John Doe"
        assert request1.email == "john@example.com"
        assert request2.name == "Jane Doe"
        assert request2.email == "jane@example.com"
        
        # Both should have same domain_id
        assert request1.domain_id == "domain123"
        assert request2.domain_id == "domain123" 