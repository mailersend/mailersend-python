"""Tests for Email Verification API builder."""

import pytest

from mailersend.builders.email_verification import EmailVerificationBuilder
from mailersend.models.email_verification import (
    EmailVerificationListsQueryParams,
    EmailVerificationResultsQueryParams,
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

    def setup_method(self):
        """Set up test fixtures."""
        self.builder = EmailVerificationBuilder()

    def test_builder_initialization(self):
        """Test builder initialization."""
        assert self.builder._email is None
        assert self.builder._email_verification_id is None
        assert self.builder._page is None
        assert self.builder._limit is None
        assert self.builder._name is None
        assert self.builder._emails is None
        assert self.builder._results is None

    def test_reset(self):
        """Test reset method."""
        self.builder.email("test@example.com").page(2).limit(50)
        self.builder.reset()
        
        assert self.builder._email is None
        assert self.builder._page is None
        assert self.builder._limit is None

    def test_copy(self):
        """Test copy method."""
        original = self.builder.email("test@example.com").page(2).limit(50)
        copy = original.copy()
        
        assert copy._email == "test@example.com"
        assert copy._page == 2
        assert copy._limit == 50
        assert copy is not original

    def test_email(self):
        """Test email method."""
        result = self.builder.email("test@example.com")
        assert self.builder._email == "test@example.com"
        assert result is self.builder

    def test_email_verification_id(self):
        """Test email_verification_id method."""
        result = self.builder.email_verification_id("abc123")
        assert self.builder._email_verification_id == "abc123"
        assert result is self.builder

    def test_page(self):
        """Test page method."""
        result = self.builder.page(2)
        assert self.builder._page == 2
        assert result is self.builder

    def test_limit(self):
        """Test limit method."""
        result = self.builder.limit(50)
        assert self.builder._limit == 50
        assert result is self.builder

    def test_name(self):
        """Test name method."""
        result = self.builder.name("Test List")
        assert self.builder._name == "Test List"
        assert result is self.builder

    def test_emails(self):
        """Test emails method."""
        emails = ["test1@example.com", "test2@example.com"]
        result = self.builder.emails(emails)
        assert self.builder._emails == emails
        assert self.builder._emails is not emails  # Should be a copy
        assert result is self.builder

    def test_add_email(self):
        """Test add_email method."""
        result = self.builder.add_email("test1@example.com")
        assert self.builder._emails == ["test1@example.com"]
        
        self.builder.add_email("test2@example.com")
        assert self.builder._emails == ["test1@example.com", "test2@example.com"]
        assert result is self.builder

    def test_results(self):
        """Test results method."""
        results = ["valid", "catch_all"]
        result = self.builder.results(results)
        assert self.builder._results == results
        assert self.builder._results is not results  # Should be a copy
        assert result is self.builder

    def test_add_result_filter(self):
        """Test add_result_filter method."""
        result = self.builder.add_result_filter("valid")
        assert self.builder._results == ["valid"]
        
        self.builder.add_result_filter("catch_all")
        assert self.builder._results == ["valid", "catch_all"]
        
        # Should not add duplicates
        self.builder.add_result_filter("valid")
        assert self.builder._results == ["valid", "catch_all"]
        assert result is self.builder

    def test_valid_results(self):
        """Test valid_results method."""
        result = self.builder.valid_results()
        assert "valid" in self.builder._results
        assert result is self.builder
        
        # Should not add duplicates
        self.builder.valid_results()
        assert self.builder._results.count("valid") == 1

    def test_risky_results(self):
        """Test risky_results method."""
        result = self.builder.risky_results()
        risky_results = ["catch_all", "mailbox_full", "role_based", "unknown"]
        for risky_result in risky_results:
            assert risky_result in self.builder._results
        assert result is self.builder

    def test_do_not_send_results(self):
        """Test do_not_send_results method."""
        result = self.builder.do_not_send_results()
        do_not_send_results = ["syntax_error", "typo", "mailbox_not_found", "disposable", "mailbox_blocked", "failed"]
        for do_not_send_result in do_not_send_results:
            assert do_not_send_result in self.builder._results
        assert result is self.builder

    def test_all_results(self):
        """Test all_results method."""
        result = self.builder.all_results()
        
        # Should include all result types
        all_expected_results = [
            "valid", "catch_all", "mailbox_full", "role_based", "unknown",
            "syntax_error", "typo", "mailbox_not_found", "disposable", "mailbox_blocked", "failed"
        ]
        for expected_result in all_expected_results:
            assert expected_result in self.builder._results
        assert result is self.builder

    def test_build_verify_email_valid(self):
        """Test build_verify_email with valid data."""
        request = self.builder.email("test@example.com").build_verify_email()
        
        assert isinstance(request, EmailVerifyRequest)
        assert request.email == "test@example.com"

    def test_build_verify_email_missing_email(self):
        """Test build_verify_email with missing email."""
        with pytest.raises(ValueError, match="email is required for email verification request"):
            self.builder.build_verify_email()

    def test_build_verify_email_async_valid(self):
        """Test build_verify_email_async with valid data."""
        request = self.builder.email("test@example.com").build_verify_email_async()
        
        assert isinstance(request, EmailVerifyAsyncRequest)
        assert request.email == "test@example.com"

    def test_build_verify_email_async_missing_email(self):
        """Test build_verify_email_async with missing email."""
        with pytest.raises(ValueError, match="email is required for async email verification request"):
            self.builder.build_verify_email_async()

    def test_build_async_status_valid(self):
        """Test build_async_status with valid data."""
        request = self.builder.email_verification_id("abc123").build_async_status()
        
        assert isinstance(request, EmailVerificationAsyncStatusRequest)
        assert request.email_verification_id == "abc123"

    def test_build_async_status_missing_id(self):
        """Test build_async_status with missing ID."""
        with pytest.raises(ValueError, match="email_verification_id is required for async status request"):
            self.builder.build_async_status()

    def test_build_lists_with_defaults(self):
        """Test build_lists with default values."""
        request = self.builder.build_lists()
        
        assert isinstance(request, EmailVerificationListsRequest)
        assert isinstance(request.query_params, EmailVerificationListsQueryParams)
        assert request.query_params.page == 1
        assert request.query_params.limit == 25

    def test_build_lists_with_custom_params(self):
        """Test build_lists with custom parameters."""
        request = self.builder.page(2).limit(50).build_lists()
        
        assert isinstance(request, EmailVerificationListsRequest)
        assert request.query_params.page == 2
        assert request.query_params.limit == 50

    def test_build_get_valid(self):
        """Test build_get with valid data."""
        request = self.builder.email_verification_id("abc123").build_get()
        
        assert isinstance(request, EmailVerificationGetRequest)
        assert request.email_verification_id == "abc123"

    def test_build_get_missing_id(self):
        """Test build_get with missing ID."""
        with pytest.raises(ValueError, match="email_verification_id is required for get verification request"):
            self.builder.build_get()

    def test_build_create_valid(self):
        """Test build_create with valid data."""
        emails = ["test1@example.com", "test2@example.com"]
        request = self.builder.name("Test List").emails(emails).build_create()
        
        assert isinstance(request, EmailVerificationCreateRequest)
        assert request.name == "Test List"
        assert request.emails == emails

    def test_build_create_missing_name(self):
        """Test build_create with missing name."""
        with pytest.raises(ValueError, match="name is required for create verification request"):
            self.builder.emails(["test@example.com"]).build_create()

    def test_build_create_missing_emails(self):
        """Test build_create with missing emails."""
        with pytest.raises(ValueError, match="emails are required for create verification request"):
            self.builder.name("Test List").build_create()

    def test_build_verify_list_valid(self):
        """Test build_verify_list with valid data."""
        request = self.builder.email_verification_id("abc123").build_verify_list()
        
        assert isinstance(request, EmailVerificationVerifyRequest)
        assert request.email_verification_id == "abc123"

    def test_build_verify_list_missing_id(self):
        """Test build_verify_list with missing ID."""
        with pytest.raises(ValueError, match="email_verification_id is required for verify list request"):
            self.builder.build_verify_list()

    def test_build_results_with_defaults(self):
        """Test build_results with default values."""
        request = self.builder.email_verification_id("abc123").build_results()
        
        assert isinstance(request, EmailVerificationResultsRequest)
        assert request.email_verification_id == "abc123"
        assert isinstance(request.query_params, EmailVerificationResultsQueryParams)
        assert request.query_params.page == 1
        assert request.query_params.limit == 25
        assert request.query_params.results is None

    def test_build_results_with_custom_params(self):
        """Test build_results with custom parameters."""
        results = ["valid", "catch_all"]
        request = (self.builder
                   .email_verification_id("abc123")
                   .page(2)
                   .limit(50)
                   .results(results)
                   .build_results())
        
        assert isinstance(request, EmailVerificationResultsRequest)
        assert request.email_verification_id == "abc123"
        assert request.query_params.page == 2
        assert request.query_params.limit == 50
        assert request.query_params.results == results

    def test_build_results_missing_id(self):
        """Test build_results with missing ID."""
        with pytest.raises(ValueError, match="email_verification_id is required for results request"):
            self.builder.build_results()

    def test_method_chaining(self):
        """Test method chaining for fluent interface."""
        request = (self.builder
                   .email_verification_id("abc123")
                   .page(2)
                   .limit(50)
                   .valid_results()
                   .risky_results()
                   .build_results())
        
        assert isinstance(request, EmailVerificationResultsRequest)
        assert request.email_verification_id == "abc123"
        assert request.query_params.page == 2
        assert request.query_params.limit == 50
        assert "valid" in request.query_params.results
        assert "catch_all" in request.query_params.results 