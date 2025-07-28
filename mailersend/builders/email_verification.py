"""Email Verification API builder for MailerSend SDK."""

from typing import List, Optional

from ..models.email_verification import (
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


class EmailVerificationBuilder:
    """Builder for constructing email verification API requests using a fluent interface."""

    def __init__(self) -> None:
        """Initialize the EmailVerificationBuilder."""
        self.reset()

    def reset(self) -> "EmailVerificationBuilder":
        """Reset the builder to its initial state.
        
        Returns:
            EmailVerificationBuilder: The builder instance for method chaining.
        """
        self._email: Optional[str] = None
        self._email_verification_id: Optional[str] = None
        self._page: Optional[int] = None
        self._limit: Optional[int] = None
        self._name: Optional[str] = None
        self._emails: Optional[List[str]] = None
        self._results: Optional[List[str]] = None
        return self

    def copy(self) -> "EmailVerificationBuilder":
        """Create a copy of the current builder state.
        
        Returns:
            EmailVerificationBuilder: A new builder instance with the same state.
        """
        new_builder = EmailVerificationBuilder()
        new_builder._email = self._email
        new_builder._email_verification_id = self._email_verification_id
        new_builder._page = self._page
        new_builder._limit = self._limit
        new_builder._name = self._name
        new_builder._emails = self._emails.copy() if self._emails else None
        new_builder._results = self._results.copy() if self._results else None
        return new_builder

    def email(self, email: str) -> "EmailVerificationBuilder":
        """Set the email address to verify.
        
        Args:
            email: Email address to verify.
            
        Returns:
            EmailVerificationBuilder: The builder instance for method chaining.
        """
        self._email = email
        return self

    def email_verification_id(self, email_verification_id: str) -> "EmailVerificationBuilder":
        """Set the email verification ID.
        
        Args:
            email_verification_id: Email verification ID.
            
        Returns:
            EmailVerificationBuilder: The builder instance for method chaining.
        """
        self._email_verification_id = email_verification_id
        return self

    def page(self, page: int) -> "EmailVerificationBuilder":
        """Set the page number for pagination.
        
        Args:
            page: Page number (must be >= 1).
            
        Returns:
            EmailVerificationBuilder: The builder instance for method chaining.
        """
        self._page = page
        return self

    def limit(self, limit: int) -> "EmailVerificationBuilder":
        """Set the items per page limit.
        
        Args:
            limit: Number of items per page (10-100).
            
        Returns:
            EmailVerificationBuilder: The builder instance for method chaining.
        """
        self._limit = limit
        return self

    def name(self, name: str) -> "EmailVerificationBuilder":
        """Set the name for verification list.
        
        Args:
            name: Name of the verification list.
            
        Returns:
            EmailVerificationBuilder: The builder instance for method chaining.
        """
        self._name = name
        return self

    def emails(self, emails: List[str]) -> "EmailVerificationBuilder":
        """Set the list of emails for verification.
        
        Args:
            emails: List of email addresses to verify.
            
        Returns:
            EmailVerificationBuilder: The builder instance for method chaining.
        """
        self._emails = emails.copy() if emails else []
        return self

    def add_email(self, email: str) -> "EmailVerificationBuilder":
        """Add a single email to the verification list.
        
        Args:
            email: Email address to add.
            
        Returns:
            EmailVerificationBuilder: The builder instance for method chaining.
        """
        if self._emails is None:
            self._emails = []
        self._emails.append(email)
        return self

    def results(self, results: List[str]) -> "EmailVerificationBuilder":
        """Set the results filter for querying verification results.
        
        Args:
            results: List of result types to filter by.
            
        Returns:
            EmailVerificationBuilder: The builder instance for method chaining.
        """
        self._results = results.copy() if results else []
        return self

    def add_result_filter(self, result: str) -> "EmailVerificationBuilder":
        """Add a single result filter.
        
        Args:
            result: Result type to filter by.
            
        Returns:
            EmailVerificationBuilder: The builder instance for method chaining.
        """
        if self._results is None:
            self._results = []
        if result not in self._results:
            self._results.append(result)
        return self

    def valid_results(self) -> "EmailVerificationBuilder":
        """Add all valid email result filters.
        
        Returns:
            EmailVerificationBuilder: The builder instance for method chaining.
        """
        if self._results is None:
            self._results = []
        if "valid" not in self._results:
            self._results.append("valid")
        return self

    def risky_results(self) -> "EmailVerificationBuilder":
        """Add all risky email result filters.
        
        Returns:
            EmailVerificationBuilder: The builder instance for method chaining.
        """
        if self._results is None:
            self._results = []
        risky_results = ["catch_all", "mailbox_full", "role_based", "unknown"]
        for result in risky_results:
            if result not in self._results:
                self._results.append(result)
        return self

    def do_not_send_results(self) -> "EmailVerificationBuilder":
        """Add all 'do not send' email result filters.
        
        Returns:
            EmailVerificationBuilder: The builder instance for method chaining.
        """
        if self._results is None:
            self._results = []
        do_not_send_results = ["syntax_error", "typo", "mailbox_not_found", "disposable", "mailbox_blocked", "failed"]
        for result in do_not_send_results:
            if result not in self._results:
                self._results.append(result)
        return self

    def all_results(self) -> "EmailVerificationBuilder":
        """Add all email result filters.
        
        Returns:
            EmailVerificationBuilder: The builder instance for method chaining.
        """
        self.valid_results()
        self.risky_results()
        self.do_not_send_results()
        return self

    def build_verify_email(self) -> EmailVerifyRequest:
        """Build EmailVerifyRequest from current builder state.
        
        Returns:
            EmailVerifyRequest: Constructed request object
            
        Raises:
            ValueError: If required fields are missing
        """
        if not self._email:
            raise ValueError("email is required for email verification request")
        
        return EmailVerifyRequest(email=self._email)

    def build_verify_email_async(self) -> EmailVerifyAsyncRequest:
        """Build EmailVerifyAsyncRequest from current builder state.
        
        Returns:
            EmailVerifyAsyncRequest: Constructed request object
            
        Raises:
            ValueError: If required fields are missing
        """
        if not self._email:
            raise ValueError("email is required for async email verification request")
        
        return EmailVerifyAsyncRequest(email=self._email)

    def build_async_status(self) -> EmailVerificationAsyncStatusRequest:
        """Build EmailVerificationAsyncStatusRequest from current builder state.
        
        Returns:
            EmailVerificationAsyncStatusRequest: Constructed request object
            
        Raises:
            ValueError: If required fields are missing
        """
        if not self._email_verification_id:
            raise ValueError("email_verification_id is required for async status request")
        
        return EmailVerificationAsyncStatusRequest(email_verification_id=self._email_verification_id)

    def build_lists(self) -> EmailVerificationListsRequest:
        """Build EmailVerificationListsRequest from current builder state.
        
        Returns:
            EmailVerificationListsRequest: Constructed request object
        """
        # Create query params with defaults and builder values
        query_params_data = {}
        if self._page is not None:
            query_params_data["page"] = self._page
        if self._limit is not None:
            query_params_data["limit"] = self._limit
        
        query_params = EmailVerificationListsQueryParams(**query_params_data)
        
        return EmailVerificationListsRequest(query_params=query_params)

    def build_get(self) -> EmailVerificationGetRequest:
        """Build EmailVerificationGetRequest from current builder state.
        
        Returns:
            EmailVerificationGetRequest: Constructed request object
            
        Raises:
            ValueError: If required fields are missing
        """
        if not self._email_verification_id:
            raise ValueError("email_verification_id is required for get verification request")
        
        return EmailVerificationGetRequest(email_verification_id=self._email_verification_id)

    def build_create(self) -> EmailVerificationCreateRequest:
        """Build EmailVerificationCreateRequest from current builder state.
        
        Returns:
            EmailVerificationCreateRequest: Constructed request object
            
        Raises:
            ValueError: If required fields are missing
        """
        if not self._name:
            raise ValueError("name is required for create verification request")
        if not self._emails:
            raise ValueError("emails are required for create verification request")
        
        return EmailVerificationCreateRequest(
            name=self._name,
            emails=self._emails
        )

    def build_verify_list(self) -> EmailVerificationVerifyRequest:
        """Build EmailVerificationVerifyRequest from current builder state.
        
        Returns:
            EmailVerificationVerifyRequest: Constructed request object
            
        Raises:
            ValueError: If required fields are missing
        """
        if not self._email_verification_id:
            raise ValueError("email_verification_id is required for verify list request")
        
        return EmailVerificationVerifyRequest(email_verification_id=self._email_verification_id)

    def build_results(self) -> EmailVerificationResultsRequest:
        """Build EmailVerificationResultsRequest from current builder state.
        
        Returns:
            EmailVerificationResultsRequest: Constructed request object
            
        Raises:
            ValueError: If required fields are missing
        """
        if not self._email_verification_id:
            raise ValueError("email_verification_id is required for results request")
        
        # Create query params with defaults and builder values
        query_params_data = {}
        if self._page is not None:
            query_params_data["page"] = self._page
        if self._limit is not None:
            query_params_data["limit"] = self._limit
        if self._results is not None:
            query_params_data["results"] = self._results
        
        query_params = EmailVerificationResultsQueryParams(**query_params_data)
        
        return EmailVerificationResultsRequest(
            email_verification_id=self._email_verification_id,
            query_params=query_params
        ) 