"""Email models."""

from typing import List, Dict, Optional, Any, Union
from pydantic import (
    Field,
    EmailStr,
    ConfigDict,
    field_validator,
    model_validator,
)
from .base import BaseModel
import time


class EmailContact(BaseModel):
    email: EmailStr
    name: Optional[str] = None


class EmailAttachment(BaseModel):
    content: str  # Base64 encoded content
    disposition: str  # 'inline' or 'attachment'
    filename: str
    id: Optional[str] = None

    @field_validator("disposition")
    def validate_disposition(cls, v):
        if v not in ["inline", "attachment"]:
            raise ValueError("Disposition must be 'inline' or 'attachment'")
        return v


class EmailPersonalization(BaseModel):
    email: EmailStr
    data: Dict[str, Any]


class EmailTrackingSettings(BaseModel):
    track_clicks: Optional[bool] = None
    track_opens: Optional[bool] = None
    track_content: Optional[bool] = None


class EmailHeader(BaseModel):
    name: str
    value: str

    @field_validator("name")
    def validate_name(cls, v):
        if not v.replace("-", "").isalnum():
            raise ValueError("Header name must be alphanumeric and may contain '-'")
        return v


class EmailRequest(BaseModel):
    from_email: Optional[EmailContact] = Field(None, alias="from")
    to: List[EmailContact]
    cc: Optional[List[EmailContact]] = None
    bcc: Optional[List[EmailContact]] = None
    reply_to: Optional[EmailContact] = None
    subject: str
    text: Optional[str] = None
    html: Optional[str] = None
    template_id: Optional[str] = None
    language: Optional[str] = None
    attachments: Optional[List[EmailAttachment]] = None
    tags: Optional[List[str]] = None
    personalization: Optional[List[EmailPersonalization]] = None
    precedence_bulk: Optional[bool] = None
    send_at: Optional[int] = None
    in_reply_to: Optional[EmailStr] = None
    references: Optional[List[str]] = None
    settings: Optional[EmailTrackingSettings] = None
    headers: Optional[List[EmailHeader]] = None

    model_config = ConfigDict(validate_by_name=True)

    @model_validator(mode="after")
    def validate_from_email(self):
        if self.from_email is None and self.template_id is None:
            raise ValueError(
                "At least one of 'from_email' or 'template_id' is required"
            )
        return self

    @field_validator("subject")
    def validate_subject_length(cls, v):
        if v and len(v) > 998:
            raise ValueError("Subject must be less than 998 characters")
        return v

    @model_validator(mode="after")
    def validate_content_exists(self):
        if self.html is None and self.text is None and self.template_id is None:
            raise ValueError(
                "At least one of 'text', 'html' or 'template_id' must be provided"
            )
        return self

    @field_validator("tags")
    def validate_tags_count(cls, v):
        if v and len(v) > 5:
            raise ValueError("Maximum 5 tags are allowed")
        return v

    @field_validator("to")
    def validate_to_count(cls, v):
        if len(v) < 1 or len(v) > 50:
            raise ValueError("'to' must contain between 1 and 50 recipients")
        return v

    @field_validator("cc", "bcc")
    def validate_cc_bcc_count(cls, v):
        if v and len(v) > 10:
            raise ValueError("Maximum 10 recipients allowed for cc/bcc")
        return v

    @field_validator("send_at")
    def validate_send_at(cls, v):
        current_time = int(time.time())
        if v and (v < current_time or v > current_time + 259200):
            raise ValueError("send_at must be between now and 72 hours from now")
        return v


EMAIL_STATUSES = {"queued", "sent", "rejected", "delivered"}

EMAIL_INTERACTIONS = {
    "opened",
    "clicked",
    "unsubscribed",
    "complained",
    "no_interaction",
}


class EmailActivityEvent(BaseModel):
    """Model for a single activity event returned with an email."""

    id: str
    type: str  # Event type (queued, sent, delivered, opened, ...)
    created_at: str
    # Present only for "suppressed" events: on_hold, hard_bounced,
    # unsubscribed, spam_complained, blocklisted
    suppression_reason: Optional[str] = None

    model_config = ConfigDict(validate_by_name=True)


class EmailListItem(BaseModel):
    """Model for a single email row returned by the emails list endpoint."""

    id: str
    from_email: EmailStr = Field(alias="from")
    to: str
    # Content is never returned in list rows, only by the single email endpoint
    text: Optional[str] = None
    html: Optional[str] = None
    subject: str
    template_id: Optional[str] = None
    domain_id: str
    message_id: str
    status: str  # One of queued, sent, rejected, delivered
    tags: Optional[List[str]] = None
    interaction: List[str] = Field(default_factory=list)
    # Only set when status is "rejected"
    suppression_reason: Optional[str] = None
    created_at: str
    updated_at: str
    headers: Optional[List[EmailHeader]] = None

    model_config = ConfigDict(validate_by_name=True)


class EmailsListQueryParams(BaseModel):
    """
    Model for emails list query parameters with validation.

    Paginated with ``page`` and ``limit``, the same way as
    ``GET /v1/activity``.
    """

    domain_id: str
    date_from: Union[int, str]  # Unix timestamp or datetime string
    date_to: Union[int, str]  # Unix timestamp or datetime string
    page: Optional[int] = Field(default=1, ge=1, le=100)
    limit: Optional[int] = Field(default=25, ge=10, le=1000)
    status: Optional[List[str]] = None
    interaction: Optional[List[str]] = None
    recipient_email: Optional[EmailStr] = None
    message_id: Optional[str] = None
    template_id: Optional[str] = None
    subject: Optional[str] = Field(default=None, min_length=3)
    tag: Optional[str] = None

    model_config = ConfigDict(validate_by_name=True)

    @field_validator("domain_id")
    def validate_domain_id(cls, v):
        if not v or not v.strip():
            raise ValueError("domain_id is required")
        return v.strip()

    @field_validator("message_id")
    def validate_message_id(cls, v):
        if v is not None and not v.isalnum():
            raise ValueError("message_id must be alphanumeric")
        return v

    @field_validator("status")
    def validate_status(cls, v):
        if v:
            invalid = set(v) - EMAIL_STATUSES
            if invalid:
                raise ValueError(f"Invalid status values: {invalid}")
        return v

    @field_validator("interaction")
    def validate_interaction(cls, v):
        if v:
            invalid = set(v) - EMAIL_INTERACTIONS
            if invalid:
                raise ValueError(f"Invalid interaction values: {invalid}")
        return v

    def model_post_init(self, __context: Any) -> None:
        """Post-initialization validation."""
        # Only comparable when both dates were given as unix timestamps
        if isinstance(self.date_from, int) and isinstance(self.date_to, int):
            if self.date_to <= self.date_from:
                raise ValueError("date_to must be greater than date_from")

    def to_query_params(self) -> dict:
        """Convert to query parameters for API request."""
        params = {
            "domain_id": self.domain_id,
            "date_from": self.date_from,
            "date_to": self.date_to,
            "page": self.page,
            "limit": self.limit,
            "recipient_email": self.recipient_email,
            "message_id": self.message_id,
            "template_id": self.template_id,
            "subject": self.subject,
            "tag": self.tag,
        }

        # status and interaction must always be sent as arrays
        for name in ("status", "interaction"):
            values = getattr(self, name)
            if values:
                for i, value in enumerate(values):
                    params[f"{name}[{i}]"] = value

        return {k: v for k, v in params.items() if v is not None}


class EmailsListRequest(BaseModel):
    """Request model for listing emails."""

    query_params: EmailsListQueryParams

    model_config = ConfigDict(validate_by_name=True)

    def to_query_params(self) -> dict:
        """Convert query parameters for API request."""
        return self.query_params.to_query_params()


class EmailGetRequest(BaseModel):
    """Request model for getting a single email with its activity."""

    email_id: str

    model_config = ConfigDict(validate_by_name=True)

    @field_validator("email_id")
    def validate_email_id(cls, v):
        if not v or not v.strip():
            raise ValueError("email_id is required")
        return v.strip()
