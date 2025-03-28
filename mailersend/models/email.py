from datetime import datetime
from typing import List, Dict, Any, Optional, Union
from pydantic import BaseModel, Field, EmailStr, HttpUrl, validator


class EmailRecipient(BaseModel):
    """
    Represents an email recipient (to, cc, bcc).
    """
    email: EmailStr
    name: Optional[str] = None


class EmailFrom(BaseModel):
    """
    Represents the email sender.
    """
    email: EmailStr
    name: Optional[str] = None


class EmailPersonalization(BaseModel):
    """
    Represents personalization variables for an email.
    """
    email: EmailStr
    data: Dict[str, Any]

    class Config:
        arbitrary_types_allowed = True


class EmailAttachment(BaseModel):
    """
    Represents an email attachment.
    """
    content: str  # Base64 encoded
    filename: str
    disposition: Optional[str] = "attachment"
    id: Optional[str] = None


class EmailTemplate(BaseModel):
    """
    Represents an email template.
    """
    id: str
    variables: Optional[Dict[str, Any]] = None


class EmailTracking(BaseModel):
    """
    Represents email tracking settings.
    """
    opens: Optional[bool] = True
    clicks: Optional[bool] = True
    unsubscribe: Optional[bool] = True


class EmailSettings(BaseModel):
    """
    Represents email send settings.
    """
    tracking: Optional[EmailTracking] = None
    tags: Optional[List[str]] = None
    precedence_bulk: Optional[bool] = None
    send_at: Optional[datetime] = None


class EmailRequest(BaseModel):
    """
    Represents a complete email send request.
    """
    from_email: EmailFrom = Field(..., alias="from")
    to: List[EmailRecipient]
    subject: str
    text: Optional[str] = None
    html: Optional[str] = None
    cc: Optional[List[EmailRecipient]] = None
    bcc: Optional[List[EmailRecipient]] = None
    reply_to: Optional[EmailRecipient] = None
    attachments: Optional[List[EmailAttachment]] = None
    template_id: Optional[str] = None
    personalization: Optional[List[EmailPersonalization]] = None
    tags: Optional[List[str]] = None
    tracking: Optional[EmailTracking] = None
    precedence_bulk: Optional[bool] = None
    send_at: Optional[int] = None
    in_reply_to: Optional[str] = None
    references: Optional[str] = None
    settings: Optional[EmailSettings] = None
    headers: Optional[EmailHeaders] = None

    @validator('html', 'text', always=True)
    def validate_content(cls, v, values):
        """Validate that either html, text or template_id is provided."""
        if not v and not values.get('text') and not values.get('html') and not values.get('template_id'):
            raise ValueError('Either html, text, or template_id must be provided')
        return v

    class Config:
        allow_population_by_field_name = True


class BulkEmailRequest(BaseModel):
    """
    Represents a bulk email send request.
    """
    to: List[EmailRecipient]
    mail_settings: Optional[EmailSettings] = None


class EmailStatus(BaseModel):
    """
    Represents the status of an email.
    """
    id: str
    status: str
    created_at: datetime
    updated_at: Optional[datetime] = None


class EmailActivity(BaseModel):
    """
    Represents an email activity event.
    """
    id: str
    type: str
    email_id: str
    created_at: datetime
    domain_id: str
    recipient: Dict[str, Any]