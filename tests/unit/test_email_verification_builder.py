"""Tests for Email Verification API builder."""

import pytest

from mailersend.builders.email_verification import EmailVerificationBuilder
from mailersend.models.email_verification import (
    EmailVerifyRequest,
    EmailVerifyAsyncRequest,
    EmailVerificationAsyncStatusRequest,
    EmailVerificationListsRequest,
    EmailVerificationGetRequest,
    EmailVerificationCreateRequest,
    EmailVerificationVerifyRequest,
    EmailVerificationResultsRequest,
)


class TestEmailVerificationBuilder:
    """Test EmailVerificationBuilder class."""

    def test_initialization(self):
        """Test builder initialization."""
        builder = EmailVerificationBuilder()
        assert builder._email is None
        assert builder._email_verification_id is None
        assert builder._page is None
        assert builder._limit is None
        assert builder._name is None
        assert builder._emails is None
        assert builder._results is None

    def test_reset(self):
        """Test reset functionality."""
        builder = EmailVerificationBuilder()
        builder.email("test@example.com").page(2).limit(50)
        
        # Reset should clear all values
        builder.reset()
        assert builder._email is None
        assert builder._page is None
        assert builder._limit is None

    def test_copy(self):
        """Test copy functionality."""
        original = EmailVerificationBuilder()
        original.email("test@example.com").page(2).emails(["test1@example.com", "test2@example.com"])
        
        copied = original.copy()
        
        # Should have same values
        assert copied._email == original._email
        assert copied._page == original._page
        assert copied._emails == original._emails
        
        # Should be independent instances
        copied.email("different@example.com")
        assert copied._email != original._email
        assert original._email == "test@example.com"

    def test_email_method(self):
        """Test email method."""
        builder = EmailVerificationBuilder()
        result = builder.email("test@example.com")
        
        assert result is builder  # Should return self for chaining
        assert builder._email == "test@example.com"

    def test_email_verification_id_method(self):
        """Test email_verification_id method."""
        builder = EmailVerificationBuilder()
        result = builder.email_verification_id("abc123")
        
        assert result is builder
        assert builder._email_verification_id == "abc123"

    def test_page_method(self):
        """Test page method."""
        builder = EmailVerificationBuilder()
        result = builder.page(2)
        
        assert result is builder
        assert builder._page == 2

    def test_limit_method(self):
        """Test limit method."""
        builder = EmailVerificationBuilder()
        result = builder.limit(50)
        
        assert result is builder
        assert builder._limit == 50

    def test_name_method(self):
        """Test name method."""
        builder = EmailVerificationBuilder()
        result = builder.name("Test List")
        
        assert result is builder
        assert builder._name == "Test List"

    def test_emails_method(self):
        """Test emails method."""
        builder = EmailVerificationBuilder()
        emails = ["test1@example.com", "test2@example.com"]
        result = builder.emails(emails)
        
        assert result is builder
        assert builder._emails == emails
        # Should be a copy, not the same list
        assert builder._emails is not emails

    def test_add_email_method(self):
        """Test add_email method."""
        builder = EmailVerificationBuilder()
        
        # First email should initialize the list
        result = builder.add_email("test1@example.com")
        assert result is builder
        assert builder._emails == ["test1@example.com"]
        
        # Second email should be appended
        builder.add_email("test2@example.com")
        assert builder._emails == ["test1@example.com", "test2@example.com"]

    def test_results_method(self):
        """Test results method."""
        builder = EmailVerificationBuilder()
        results = ["valid", "typo"]
        result = builder.results(results)
        
        assert result is builder
        assert builder._results == results
        # Should be a copy, not the same list
        assert builder._results is not results

    def test_add_result_filter_method(self):
        """Test add_result_filter method."""
        builder = EmailVerificationBuilder()
        
        # First filter should initialize the list
        result = builder.add_result_filter("valid")
        assert result is builder
        assert builder._results == ["valid"]
        
        # Second filter should be appended
        builder.add_result_filter("typo")
        assert builder._results == ["valid", "typo"]
        
        # Duplicate filters should not be added
        builder.add_result_filter("valid")
        assert builder._results == ["valid", "typo"]

    def test_valid_results_method(self):
        """Test valid_results method."""
        builder = EmailVerificationBuilder()
        result = builder.valid_results()
        
        assert result is builder
        assert "valid" in builder._results

    def test_risky_results_method(self):
        """Test risky_results method."""
        builder = EmailVerificationBuilder()
        result = builder.risky_results()
        
        assert result is builder
        expected_risky = ["catch_all", "mailbox_full", "role_based", "unknown"]
        for risky_result in expected_risky:
            assert risky_result in builder._results

    def test_do_not_send_results_method(self):
        """Test do_not_send_results method."""
        builder = EmailVerificationBuilder()
        result = builder.do_not_send_results()
        
        assert result is builder
        expected_do_not_send = ["syntax_error", "typo", "mailbox_not_found", "disposable", "mailbox_blocked"]
        for do_not_send_result in expected_do_not_send:
            assert do_not_send_result in builder._results

    def test_all_results_method(self):
        """Test all_results method."""
        builder = EmailVerificationBuilder()
        result = builder.all_results()
        
        assert result is builder
        expected_all = [
            "valid", "catch_all", "mailbox_full", "role_based", "unknown", "failed",
            "syntax_error", "typo", "mailbox_not_found", "disposable", "mailbox_blocked"
        ]
        assert builder._results == expected_all

    def test_method_chaining(self):
        """Test method chaining works correctly."""
        builder = EmailVerificationBuilder()
        result = (builder
                 .email("test@example.com")
                 .page(2)
                 .limit(50)
                 .name("Test List")
                 .add_email("test1@example.com")
                 .add_email("test2@example.com")
                 .valid_results())
        
        assert result is builder
        assert builder._email == "test@example.com"
        assert builder._page == 2
        assert builder._limit == 50
        assert builder._name == "Test List"
        assert builder._emails == ["test1@example.com", "test2@example.com"]
        assert "valid" in builder._results

    def test_build_verify_email_success(self):
        """Test successful build_verify_email."""
        builder = EmailVerificationBuilder()
        builder.email("test@example.com")
        
        request = builder.build_verify_email()
        
        assert isinstance(request, EmailVerifyRequest)
        assert request.email == "test@example.com"

    def test_build_verify_email_missing_email(self):
        """Test build_verify_email fails without email."""
        builder = EmailVerificationBuilder()
        
        with pytest.raises(ValueError) as excinfo:
            builder.build_verify_email()
        assert "email is required for email verification" in str(excinfo.value)

    def test_build_verify_email_async_success(self):
        """Test successful build_verify_email_async."""
        builder = EmailVerificationBuilder()
        builder.email("test@example.com")
        
        request = builder.build_verify_email_async()
        
        assert isinstance(request, EmailVerifyAsyncRequest)
        assert request.email == "test@example.com"

    def test_build_verify_email_async_missing_email(self):
        """Test build_verify_email_async fails without email."""
        builder = EmailVerificationBuilder()
        
        with pytest.raises(ValueError) as excinfo:
            builder.build_verify_email_async()
        assert "email is required for async email verification" in str(excinfo.value)

    def test_build_async_status_success(self):
        """Test successful build_async_status."""
        builder = EmailVerificationBuilder()
        builder.email_verification_id("abc123")
        
        request = builder.build_async_status()
        
        assert isinstance(request, EmailVerificationAsyncStatusRequest)
        assert request.email_verification_id == "abc123"

    def test_build_async_status_missing_id(self):
        """Test build_async_status fails without ID."""
        builder = EmailVerificationBuilder()
        
        with pytest.raises(ValueError) as excinfo:
            builder.build_async_status()
        assert "email_verification_id is required for async status check" in str(excinfo.value)

    def test_build_lists_success(self):
        """Test successful build_lists."""
        builder = EmailVerificationBuilder()
        builder.page(2).limit(50)
        
        request = builder.build_lists()
        
        assert isinstance(request, EmailVerificationListsRequest)
        assert request.page == 2
        assert request.limit == 50

    def test_build_lists_minimal(self):
        """Test build_lists with minimal parameters."""
        builder = EmailVerificationBuilder()
        
        request = builder.build_lists()
        
        assert isinstance(request, EmailVerificationListsRequest)
        assert request.page is None
        assert request.limit is None

    def test_build_get_success(self):
        """Test successful build_get."""
        builder = EmailVerificationBuilder()
        builder.email_verification_id("abc123")
        
        request = builder.build_get()
        
        assert isinstance(request, EmailVerificationGetRequest)
        assert request.email_verification_id == "abc123"

    def test_build_get_missing_id(self):
        """Test build_get fails without ID."""
        builder = EmailVerificationBuilder()
        
        with pytest.raises(ValueError) as excinfo:
            builder.build_get()
        assert "email_verification_id is required for getting verification list" in str(excinfo.value)

    def test_build_create_success(self):
        """Test successful build_create."""
        builder = EmailVerificationBuilder()
        builder.name("Test List").emails(["test1@example.com", "test2@example.com"])
        
        request = builder.build_create()
        
        assert isinstance(request, EmailVerificationCreateRequest)
        assert request.name == "Test List"
        assert request.emails == ["test1@example.com", "test2@example.com"]

    def test_build_create_missing_name(self):
        """Test build_create fails without name."""
        builder = EmailVerificationBuilder()
        builder.emails(["test@example.com"])
        
        with pytest.raises(ValueError) as excinfo:
            builder.build_create()
        assert "name is required for creating verification list" in str(excinfo.value)

    def test_build_create_missing_emails(self):
        """Test build_create fails without emails."""
        builder = EmailVerificationBuilder()
        builder.name("Test List")
        
        with pytest.raises(ValueError) as excinfo:
            builder.build_create()
        assert "emails list is required for creating verification list" in str(excinfo.value)

    def test_build_verify_list_success(self):
        """Test successful build_verify_list."""
        builder = EmailVerificationBuilder()
        builder.email_verification_id("abc123")
        
        request = builder.build_verify_list()
        
        assert isinstance(request, EmailVerificationVerifyRequest)
        assert request.email_verification_id == "abc123"

    def test_build_verify_list_missing_id(self):
        """Test build_verify_list fails without ID."""
        builder = EmailVerificationBuilder()
        
        with pytest.raises(ValueError) as excinfo:
            builder.build_verify_list()
        assert "email_verification_id is required for verifying list" in str(excinfo.value)

    def test_build_results_success(self):
        """Test successful build_results."""
        builder = EmailVerificationBuilder()
        builder.email_verification_id("abc123").page(2).limit(25).results(["valid", "typo"])
        
        request = builder.build_results()
        
        assert isinstance(request, EmailVerificationResultsRequest)
        assert request.email_verification_id == "abc123"
        assert request.page == 2
        assert request.limit == 25
        assert request.results == ["valid", "typo"]

    def test_build_results_minimal(self):
        """Test build_results with minimal parameters."""
        builder = EmailVerificationBuilder()
        builder.email_verification_id("abc123")
        
        request = builder.build_results()
        
        assert isinstance(request, EmailVerificationResultsRequest)
        assert request.email_verification_id == "abc123"
        assert request.page is None
        assert request.limit is None
        assert request.results is None

    def test_build_results_missing_id(self):
        """Test build_results fails without ID."""
        builder = EmailVerificationBuilder()
        
        with pytest.raises(ValueError) as excinfo:
            builder.build_results()
        assert "email_verification_id is required for getting verification results" in str(excinfo.value)

    def test_result_filter_combinations(self):
        """Test combinations of result filter methods."""
        builder = EmailVerificationBuilder()
        
        # Test combining different filter types
        result = builder.valid_results().risky_results().do_not_send_results()
        
        assert result is builder
        # Should have all result types
        expected_all = [
            "valid", "catch_all", "mailbox_full", "role_based", "unknown",
            "syntax_error", "typo", "mailbox_not_found", "disposable", "mailbox_blocked"
        ]
        for expected in expected_all:
            assert expected in builder._results

    def test_builder_reuse_after_build(self):
        """Test that builder can be reused after building a request."""
        builder = EmailVerificationBuilder()
        
        # Build first request
        builder.email("test1@example.com")
        request1 = builder.build_verify_email()
        assert request1.email == "test1@example.com"
        
        # Modify builder and build second request
        builder.email("test2@example.com")
        request2 = builder.build_verify_email()
        assert request2.email == "test2@example.com"
        
        # First request should be unchanged
        assert request1.email == "test1@example.com" 