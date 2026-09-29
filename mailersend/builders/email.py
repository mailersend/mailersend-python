"""
Email Builder - Fluent API for constructing complex email requests.

This module provides the EmailBuilder class which offers a chainable,
developer-friendly API for building complex email requests with
intelligent defaults, file handling, and validation.
"""

import base64
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Dict, Any, Optional, Union

from ..models.email import (
    EmailRequest,
    EmailContact,
    EmailAttachment,
    EmailPersonalization,
    EmailTrackingSettings,
    EmailHeader,
    EmailsListQueryParams,
    EmailsListRequest,
    EmailGetRequest,
)
from ..exceptions import ValidationError


class EmailBuilder:
    """
    Fluent builder for constructing EmailRequest objects.

    Provides a chainable API that makes it easy to build complex emails
    with attachments, personalization, tracking settings, and more.

    Examples:
        >>> # Simple email
        >>> email = (EmailBuilder()
        ...     .from_email("sender@example.com", "Sender Name")
        ...     .to("recipient@example.com")
        ...     .subject("Hello World")
        ...     .html("<h1>Hello!</h1>")
        ...     .build())

        >>> # Complex email with all features
        >>> email = (EmailBuilder()
        ...     .from_email("sender@example.com", "Marketing Team")
        ...     .to("user1@example.com", "John Doe")
        ...     .to("user2@example.com", "Jane Smith")
        ...     .cc("manager@example.com")
        ...     .bcc([
        ...         {"email": "analytics@example.com", "name": "Analytics Team"},
        ...         {"email": "backup@example.com"}
        ...     ])
        ...     .subject("Monthly Newsletter")
        ...     .html_file("templates/newsletter.html")
        ...     .attach_file("documents/report.pdf")
        ...     .personalize("user1@example.com", name="John", company="Acme")
        ...     .tag("newsletter", "monthly")
        ...     .track_clicks(True)
        ...     .header("X-Campaign-ID", "newsletter-2024-01")
        ...     .build())
    """

    def __init__(self):
        """Initialize a new EmailBuilder."""
        self._from_email: Optional[EmailContact] = None
        self._to: List[EmailContact] = []
        self._cc: List[EmailContact] = []
        self._bcc: List[EmailContact] = []
        self._reply_to: Optional[EmailContact] = None
        self._subject: Optional[str] = None
        self._html: Optional[str] = None
        self._text: Optional[str] = None
        self._template_id: Optional[str] = None
        self._language: Optional[str] = None
        self._attachments: List[EmailAttachment] = []
        self._tags: List[str] = []
        self._personalization: List[EmailPersonalization] = []
        self._precedence_bulk: Optional[bool] = None
        self._send_at: Optional[int] = None
        self._in_reply_to: Optional[str] = None
        self._references: List[str] = []
        self._settings: Optional[EmailTrackingSettings] = None
        self._headers: List[EmailHeader] = []

    def from_email(self, email: str, name: Optional[str] = None) -> "EmailBuilder":
        """
        Set the sender email address.

        Args:
            email: Sender email address
            name: Optional sender name

        Returns:
            EmailBuilder instance for chaining
        """
        self._from_email = EmailContact(email=email, name=name)
        return self

    def to(self, email: str, name: Optional[str] = None) -> "EmailBuilder":
        """
        Add a recipient to the TO field.

        Args:
            email: Recipient email address
            name: Optional recipient name

        Returns:
            EmailBuilder instance for chaining
        """
        self._to.append(EmailContact(email=email, name=name))
        return self

    def to_many(self, recipients: List[Dict[str, str]]) -> "EmailBuilder":
        """
        Add multiple recipients to the TO field.

        Args:
            recipients: List of dicts with 'email' and optional 'name' keys

        Returns:
            EmailBuilder instance for chaining

        Example:
            >>> builder.to_many([
            ...     {"email": "user1@example.com", "name": "User 1"},
            ...     {"email": "user2@example.com", "name": "User 2"}
            ... ])
        """
        for recipient in recipients:
            self._to.append(
                EmailContact(email=recipient["email"], name=recipient.get("name"))
            )
        return self

    def cc(
        self, email: Union[str, List[Dict[str, str]]], name: Optional[str] = None
    ) -> "EmailBuilder":
        """
        Add recipient(s) to the CC field.

        Args:
            email: CC recipient email address (string) or list of recipient objects
            name: Optional recipient name (only used when email is a string)

        Returns:
            EmailBuilder instance for chaining

        Examples:
            Single recipient:
            >>> builder.cc("cc@example.com", "CC User")

            Multiple recipients:
            >>> builder.cc([
            ...     {"email": "cc1@example.com", "name": "CC User 1"},
            ...     {"email": "cc2@example.com", "name": "CC User 2"}
            ... ])
        """
        if isinstance(email, str):
            self._cc.append(EmailContact(email=email, name=name))
        elif isinstance(email, list):
            for recipient in email:
                self._cc.append(
                    EmailContact(email=recipient["email"], name=recipient.get("name"))
                )
        else:
            raise ValidationError("Email must be a string or list of recipient objects")
        return self

    def bcc(
        self, email: Union[str, List[Dict[str, str]]], name: Optional[str] = None
    ) -> "EmailBuilder":
        """
        Add recipient(s) to the BCC field.

        Args:
            email: BCC recipient email address (string) or list of recipient objects
            name: Optional recipient name (only used when email is a string)

        Returns:
            EmailBuilder instance for chaining

        Examples:
            Single recipient:
            >>> builder.bcc("bcc@example.com", "BCC User")

            Multiple recipients:
            >>> builder.bcc([
            ...     {"email": "bcc1@example.com", "name": "BCC User 1"},
            ...     {"email": "bcc2@example.com", "name": "BCC User 2"}
            ... ])
        """
        if isinstance(email, str):
            self._bcc.append(EmailContact(email=email, name=name))
        elif isinstance(email, list):
            for recipient in email:
                self._bcc.append(
                    EmailContact(email=recipient["email"], name=recipient.get("name"))
                )
        else:
            raise ValidationError("Email must be a string or list of recipient objects")
        return self

    def cc_many(self, recipients: List[Dict[str, str]]) -> "EmailBuilder":
        """
        Add multiple recipients to the CC field.

        Args:
            recipients: List of dicts with 'email' and optional 'name' keys

        Returns:
            EmailBuilder instance for chaining

        Example:
            >>> builder.cc_many([
            ...     {"email": "cc1@example.com", "name": "CC User 1"},
            ...     {"email": "cc2@example.com", "name": "CC User 2"}
            ... ])
        """
        for recipient in recipients:
            self._cc.append(
                EmailContact(email=recipient["email"], name=recipient.get("name"))
            )
        return self

    def bcc_many(self, recipients: List[Dict[str, str]]) -> "EmailBuilder":
        """
        Add multiple recipients to the BCC field.

        Args:
            recipients: List of dicts with 'email' and optional 'name' keys

        Returns:
            EmailBuilder instance for chaining

        Example:
            >>> builder.bcc_many([
            ...     {"email": "bcc1@example.com", "name": "BCC User 1"},
            ...     {"email": "bcc2@example.com", "name": "BCC User 2"}
            ... ])
        """
        for recipient in recipients:
            self._bcc.append(
                EmailContact(email=recipient["email"], name=recipient.get("name"))
            )
        return self

    def reply_to(self, email: str, name: Optional[str] = None) -> "EmailBuilder":
        """
        Set the reply-to email address.

        Args:
            email: Reply-to email address
            name: Optional reply-to name

        Returns:
            EmailBuilder instance for chaining
        """
        self._reply_to = EmailContact(email=email, name=name)
        return self

    def subject(self, subject: str) -> "EmailBuilder":
        """
        Set the email subject.

        Args:
            subject: Email subject line

        Returns:
            EmailBuilder instance for chaining
        """
        self._subject = subject
        return self

    def html(self, html_content: str) -> "EmailBuilder":
        """
        Set the HTML content of the email.

        Args:
            html_content: HTML content string

        Returns:
            EmailBuilder instance for chaining
        """
        self._html = html_content
        return self

    def html_file(self, file_path: Union[str, Path]) -> "EmailBuilder":
        """
        Load HTML content from a file.

        Args:
            file_path: Path to HTML file

        Returns:
            EmailBuilder instance for chaining

        Raises:
            ValidationError: If file cannot be read
        """
        try:
            path = Path(file_path)
            self._html = path.read_text(encoding="utf-8")
        except Exception as e:
            raise ValidationError(f"Failed to read HTML file {file_path}: {str(e)}")
        return self

    def text(self, text_content: str) -> "EmailBuilder":
        """
        Set the plain text content of the email.

        Args:
            text_content: Plain text content string

        Returns:
            EmailBuilder instance for chaining
        """
        self._text = text_content
        return self

    def text_file(self, file_path: Union[str, Path]) -> "EmailBuilder":
        """
        Load plain text content from a file.

        Args:
            file_path: Path to text file

        Returns:
            EmailBuilder instance for chaining

        Raises:
            ValidationError: If file cannot be read
        """
        try:
            path = Path(file_path)
            self._text = path.read_text(encoding="utf-8")
        except Exception as e:
            raise ValidationError(f"Failed to read text file {file_path}: {str(e)}")
        return self

    def template(self, template_id: str) -> "EmailBuilder":
        """
        Use a template for the email content.

        Args:
            template_id: MailerSend template ID

        Returns:
            EmailBuilder instance for chaining
        """
        self._template_id = template_id
        return self

    def language(self, language: str) -> "EmailBuilder":
        """
        Set the language for the email content.

        Only meaningful when sending with a template; ignored for raw
        html/text sends. Supported codes: de, en, es, fr, it, lt,
        nl, pl, pt-BR.

        Args:
            language: Language code (e.g. "de", "fr", "pt-BR")

        Returns:
            EmailBuilder instance for chaining
        """
        self._language = language
        return self

    def attach_file(
        self,
        file_path: Union[str, Path],
        filename: Optional[str] = None,
        disposition: str = "attachment",
    ) -> "EmailBuilder":
        """
        Attach a file to the email.

        Args:
            file_path: Path to file to attach
            filename: Optional custom filename (defaults to actual filename)
            disposition: 'attachment' or 'inline'

        Returns:
            EmailBuilder instance for chaining

        Raises:
            ValidationError: If file cannot be read or disposition is invalid
        """
        try:
            path = Path(file_path)
            if not path.exists():
                raise ValidationError(f"File not found: {file_path}")

            # Read and encode file content
            content = base64.b64encode(path.read_bytes()).decode("utf-8")

            # Use provided filename or extract from path
            final_filename = filename or path.name

            attachment = EmailAttachment(
                content=content, filename=final_filename, disposition=disposition
            )

            self._attachments.append(attachment)

        except Exception as e:
            if isinstance(e, ValidationError):
                raise
            raise ValidationError(f"Failed to attach file {file_path}: {str(e)}")

        return self

    def attach_content(
        self, content: Union[str, bytes], filename: str, disposition: str = "attachment"
    ) -> "EmailBuilder":
        """
        Attach content directly (without reading from file).

        Args:
            content: Content to attach (string or bytes)
            filename: Filename for the attachment
            disposition: 'attachment' or 'inline'

        Returns:
            EmailBuilder instance for chaining
        """
        if isinstance(content, str):
            content = content.encode("utf-8")

        encoded_content = base64.b64encode(content).decode("utf-8")

        attachment = EmailAttachment(
            content=encoded_content, filename=filename, disposition=disposition
        )

        self._attachments.append(attachment)
        return self

    def tag(self, *tags: str) -> "EmailBuilder":
        """
        Add one or more tags to the email.

        Args:
            *tags: Tag names to add

        Returns:
            EmailBuilder instance for chaining

        Example:
            >>> builder.tag("newsletter", "marketing", "monthly")
        """
        self._tags.extend(tags)
        return self

    def personalize(self, email: str, **data: Any) -> "EmailBuilder":
        """
        Add personalization data for a specific recipient.

        Args:
            email: Recipient email address
            **data: Key-value pairs for personalization

        Returns:
            EmailBuilder instance for chaining

        Example:
            >>> builder.personalize("user@example.com", name="John", company="Acme")
        """
        personalization = EmailPersonalization(email=email, data=data)
        self._personalization.append(personalization)
        return self

    def personalize_many(
        self, personalizations: List[Dict[str, Any]]
    ) -> "EmailBuilder":
        """
        Add personalization data for multiple recipients.

        Args:
            personalizations: List of personalization objects

        Returns:
            EmailBuilder instance for chaining

        Example:
            >>> builder.personalize_many([
            ...     {"email": "user1@example.com", "data": {"name": "John"}},
            ...     {"email": "user2@example.com", "data": {"name": "Jane"}}
            ... ])
        """
        for p in personalizations:
            personalization = EmailPersonalization(email=p["email"], data=p["data"])
            self._personalization.append(personalization)
        return self

    def bulk_mode(self, enabled: bool = True) -> "EmailBuilder":
        """
        Enable or disable bulk precedence for the email.

        Args:
            enabled: Whether to enable bulk mode

        Returns:
            EmailBuilder instance for chaining
        """
        self._precedence_bulk = enabled
        return self

    def send_at(self, send_time: Union[datetime, int]) -> "EmailBuilder":
        """
        Schedule the email to be sent at a specific time.

        Args:
            send_time: When to send the email (datetime or unix timestamp)

        Returns:
            EmailBuilder instance for chaining
        """
        if isinstance(send_time, datetime):
            # Convert to UTC timestamp
            if send_time.tzinfo is None:
                send_time = send_time.replace(tzinfo=timezone.utc)
            self._send_at = int(send_time.timestamp())
        else:
            self._send_at = send_time
        return self

    def send_in(self, **kwargs) -> "EmailBuilder":
        """
        Schedule the email to be sent after a specific duration.

        Args:
            **kwargs: Duration arguments (hours, minutes, seconds, days)

        Returns:
            EmailBuilder instance for chaining

        Example:
            >>> builder.send_in(hours=2, minutes=30)  # Send in 2.5 hours
        """
        from datetime import timedelta

        now = datetime.now(timezone.utc)
        delta = timedelta(**kwargs)
        send_time = now + delta

        return self.send_at(send_time)

    def in_reply_to(self, email: str) -> "EmailBuilder":
        """
        Set the In-Reply-To email for threading.

        Args:
            email: Email address this email is replying to

        Returns:
            EmailBuilder instance for chaining
        """
        self._in_reply_to = email
        return self

    def reference(self, *message_ids: str) -> "EmailBuilder":
        """
        Add message IDs to the References header for threading.

        Args:
            *message_ids: Message IDs to reference

        Returns:
            EmailBuilder instance for chaining
        """
        self._references.extend(message_ids)
        return self

    def track_clicks(self, enabled: bool = True) -> "EmailBuilder":
        """
        Enable or disable click tracking.

        Args:
            enabled: Whether to track clicks

        Returns:
            EmailBuilder instance for chaining
        """
        if self._settings is None:
            self._settings = EmailTrackingSettings()
        self._settings.track_clicks = enabled
        return self

    def track_opens(self, enabled: bool = True) -> "EmailBuilder":
        """
        Enable or disable open tracking.

        Args:
            enabled: Whether to track opens

        Returns:
            EmailBuilder instance for chaining
        """
        if self._settings is None:
            self._settings = EmailTrackingSettings()
        self._settings.track_opens = enabled
        return self

    def track_content(self, enabled: bool = True) -> "EmailBuilder":
        """
        Enable or disable content tracking.

        Args:
            enabled: Whether to track content

        Returns:
            EmailBuilder instance for chaining
        """
        if self._settings is None:
            self._settings = EmailTrackingSettings()
        self._settings.track_content = enabled
        return self

    def tracking(
        self,
        clicks: Optional[bool] = None,
        opens: Optional[bool] = None,
        content: Optional[bool] = None,
    ) -> "EmailBuilder":
        """
        Configure all tracking settings at once.

        Args:
            clicks: Whether to track clicks
            opens: Whether to track opens
            content: Whether to track content

        Returns:
            EmailBuilder instance for chaining
        """
        self._settings = EmailTrackingSettings(
            track_clicks=clicks, track_opens=opens, track_content=content
        )
        return self

    def header(self, name: str, value: str) -> "EmailBuilder":
        """
        Add a custom header to the email.

        Args:
            name: Header name
            value: Header value

        Returns:
            EmailBuilder instance for chaining
        """
        header = EmailHeader(name=name, value=value)
        self._headers.append(header)
        return self

    def headers(self, headers_dict: Dict[str, str]) -> "EmailBuilder":
        """
        Add multiple custom headers to the email.

        Args:
            headers_dict: Dictionary of header name-value pairs

        Returns:
            EmailBuilder instance for chaining
        """
        for name, value in headers_dict.items():
            self.header(name, value)
        return self

    def build(self) -> EmailRequest:
        """
        Build and return the final EmailRequest object.

        Returns:
            Validated EmailRequest object

        Raises:
            ValidationError: If the email configuration is invalid
        """
        # Prepare data for EmailRequest
        data = {
            "to": self._to,
            "subject": self._subject,
        }

        # Add optional fields
        if self._from_email:
            data["from_email"] = self._from_email
        if self._cc:
            data["cc"] = self._cc
        if self._bcc:
            data["bcc"] = self._bcc
        if self._reply_to:
            data["reply_to"] = self._reply_to
        if self._html:
            data["html"] = self._html
        if self._text:
            data["text"] = self._text
        if self._template_id:
            data["template_id"] = self._template_id
        if self._language:
            data["language"] = self._language
        if self._attachments:
            data["attachments"] = self._attachments
        if self._tags:
            data["tags"] = self._tags
        if self._personalization:
            data["personalization"] = self._personalization
        if self._precedence_bulk is not None:
            data["precedence_bulk"] = self._precedence_bulk
        if self._send_at:
            data["send_at"] = self._send_at
        if self._in_reply_to:
            data["in_reply_to"] = self._in_reply_to
        if self._references:
            data["references"] = self._references
        if self._settings:
            data["settings"] = self._settings
        if self._headers:
            data["headers"] = self._headers

        # Create and return EmailRequest
        try:
            return EmailRequest(**data)
        except Exception as e:
            raise ValidationError(f"Failed to build email request: {str(e)}")

    def reset(self) -> "EmailBuilder":
        """
        Reset the builder to start fresh.

        Returns:
            EmailBuilder instance for chaining
        """
        self.__init__()
        return self

    def copy(self) -> "EmailBuilder":
        """
        Create a copy of the current builder state.

        Returns:
            New EmailBuilder instance with the same configuration
        """
        new_builder = EmailBuilder()

        # Copy all state
        new_builder._from_email = self._from_email
        new_builder._to = self._to.copy()
        new_builder._cc = self._cc.copy()
        new_builder._bcc = self._bcc.copy()
        new_builder._reply_to = self._reply_to
        new_builder._subject = self._subject
        new_builder._html = self._html
        new_builder._text = self._text
        new_builder._template_id = self._template_id
        new_builder._language = self._language
        new_builder._attachments = self._attachments.copy()
        new_builder._tags = self._tags.copy()
        new_builder._personalization = self._personalization.copy()
        new_builder._precedence_bulk = self._precedence_bulk
        new_builder._send_at = self._send_at
        new_builder._in_reply_to = self._in_reply_to
        new_builder._references = self._references.copy()
        new_builder._settings = self._settings
        new_builder._headers = self._headers.copy()

        return new_builder


class EmailsBuilder:
    """
    Fluent builder for constructing emails list and single email requests.

    Examples:
        >>> # List the delivered emails that were opened
        >>> request = (EmailsBuilder()
        ...     .domain_id("domain-id")
        ...     .date_from(1623073576)
        ...     .date_to(1623074976)
        ...     .limit(50)
        ...     .status(["sent", "delivered"])
        ...     .interaction(["opened"])
        ...     .build_list_request())

        >>> # Get a single email with its activity events
        >>> request = (EmailsBuilder()
        ...     .email_id("email-id")
        ...     .build_get_request())
    """

    def __init__(self):
        self._domain_id: Optional[str] = None
        self._date_from: Optional[Union[datetime, int, str]] = None
        self._date_to: Optional[Union[datetime, int, str]] = None
        self._page: Optional[int] = None
        self._limit: Optional[int] = None
        self._status: List[str] = []
        self._interaction: List[str] = []
        self._recipient_email: Optional[str] = None
        self._message_id: Optional[str] = None
        self._template_id: Optional[str] = None
        self._subject: Optional[str] = None
        self._tag: Optional[str] = None
        self._email_id: Optional[str] = None

    def domain_id(self, domain_id: str) -> "EmailsBuilder":
        """Set the domain ID to list emails for (required)."""
        self._domain_id = domain_id
        return self

    def date_from(self, date_from: Union[datetime, int, str]) -> "EmailsBuilder":
        """Set the start of the time window (required)."""
        self._date_from = date_from
        return self

    def date_to(self, date_to: Union[datetime, int, str]) -> "EmailsBuilder":
        """Set the end of the time window (required)."""
        self._date_to = date_to
        return self

    def page(self, page: int) -> "EmailsBuilder":
        """Set the page number (min 1, max 100, default 1)."""
        self._page = page
        return self

    def limit(self, limit: int) -> "EmailsBuilder":
        """Set the number of emails per page (min 10, max 1000, default 25)."""
        self._limit = limit
        return self

    def status(self, status: Union[str, List[str]]) -> "EmailsBuilder":
        """
        Set the status filter, replacing any previously set values.

        Possible values: queued, sent, rejected, delivered.
        """
        self._status = [status] if isinstance(status, str) else list(status)
        return self

    def add_status(self, status: str) -> "EmailsBuilder":
        """Add a single status to the status filter."""
        if status not in self._status:
            self._status.append(status)
        return self

    def interaction(self, interaction: Union[str, List[str]]) -> "EmailsBuilder":
        """
        Set the interaction filter, replacing any previously set values.

        Possible values: opened, clicked, unsubscribed, complained,
        no_interaction.
        """
        self._interaction = (
            [interaction] if isinstance(interaction, str) else list(interaction)
        )
        return self

    def add_interaction(self, interaction: str) -> "EmailsBuilder":
        """Add a single interaction to the interaction filter."""
        if interaction not in self._interaction:
            self._interaction.append(interaction)
        return self

    def recipient_email(self, recipient_email: str) -> "EmailsBuilder":
        """Filter by recipient email address (exact match)."""
        self._recipient_email = recipient_email
        return self

    def message_id(self, message_id: str) -> "EmailsBuilder":
        """Filter by the ID of the message that created the emails."""
        self._message_id = message_id
        return self

    def template_id(self, template_id: str) -> "EmailsBuilder":
        """Filter by template ID."""
        self._template_id = template_id
        return self

    def subject(self, subject: str) -> "EmailsBuilder":
        """Filter by subject (partial match, min 3 characters)."""
        self._subject = subject
        return self

    def tag(self, tag: str) -> "EmailsBuilder":
        """Filter by tag (exact match against the email's tags)."""
        self._tag = tag
        return self

    def email_id(self, email_id: str) -> "EmailsBuilder":
        """Set the email ID for a single email request."""
        self._email_id = email_id
        return self

    def copy(self) -> "EmailsBuilder":
        """Create a copy of this builder."""
        builder = EmailsBuilder()
        builder._domain_id = self._domain_id
        builder._date_from = self._date_from
        builder._date_to = self._date_to
        builder._page = self._page
        builder._limit = self._limit
        builder._status = self._status.copy()
        builder._interaction = self._interaction.copy()
        builder._recipient_email = self._recipient_email
        builder._message_id = self._message_id
        builder._template_id = self._template_id
        builder._subject = self._subject
        builder._tag = self._tag
        builder._email_id = self._email_id
        return builder

    def reset(self) -> "EmailsBuilder":
        """Reset all parameters."""
        self.__init__()
        return self

    def _convert_to_timestamp(
        self, value: Union[datetime, int, str]
    ) -> Union[int, str]:
        """Convert datetime to a unix timestamp, leaving other values as-is."""
        if isinstance(value, datetime):
            return int(value.timestamp())
        return value

    def build_list_request(self) -> EmailsListRequest:
        """
        Build the EmailsListRequest object for listing emails.

        Raises:
            ValidationError: If a required parameter is missing
        """
        if not self._domain_id:
            raise ValidationError("domain_id is required")
        if self._date_from is None:
            raise ValidationError("date_from is required")
        if self._date_to is None:
            raise ValidationError("date_to is required")

        query_params = EmailsListQueryParams(
            domain_id=self._domain_id,
            date_from=self._convert_to_timestamp(self._date_from),
            date_to=self._convert_to_timestamp(self._date_to),
            page=self._page,
            limit=self._limit,
            status=self._status or None,
            interaction=self._interaction or None,
            recipient_email=self._recipient_email,
            message_id=self._message_id,
            template_id=self._template_id,
            subject=self._subject,
            tag=self._tag,
        )

        return EmailsListRequest(query_params=query_params)

    def build_get_request(self) -> EmailGetRequest:
        """
        Build the EmailGetRequest object for getting a single email.

        Raises:
            ValidationError: If email_id is missing
        """
        if not self._email_id:
            raise ValidationError("email_id is required")

        return EmailGetRequest(email_id=self._email_id)
