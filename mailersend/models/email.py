from typing_extensions import Self
from typing import List, Dict, Optional, Any
from pydantic import (
    BaseModel,
    Field,
    EmailStr,
    ConfigDict,
    field_validator,
    model_validator,
)
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
    def validate_from_email(cls, v):
        if v.from_email is None and v.template_id is None:
            raise ValueError(
                "At least one of 'from_email' or 'template_id' is required"
            )
        return v

    @field_validator("subject")
    def validate_subject_length(cls, v):
        if v and len(v) > 998:
            raise ValueError("Subject must be less than 998 characters")
        return v

    @model_validator(mode="after")
    def validate_content_exists(cls, v):
        if v.html is None and v.text is None and v.template_id is None:
            raise ValueError(
                "At least one of 'text', 'html' or 'template_id' must be provided"
            )
        return v

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
