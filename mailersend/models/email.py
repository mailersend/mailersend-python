from typing_extensions import Self
from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field, EmailStr, ConfigDict, field_validator, model_validator

class EmailRecipient(BaseModel):
    email: EmailStr
    name: Optional[str] = None

    @field_validator('name')
    def validate_name(cls, v):
        if v and (';' in v or ',' in v):
            raise ValueError("Name cannot contain ';' or ','")
        return v

class EmailFrom(BaseModel):
    email: EmailStr
    name: Optional[str] = None

class EmailReplyTo(BaseModel):
    email: EmailStr
    name: Optional[str] = None

class EmailAttachment(BaseModel):
    content: str  # Base64 encoded content
    disposition: str  # 'inline' or 'attachment'
    filename: str
    id: Optional[str] = None
    
    @field_validator('disposition')
    def validate_disposition(cls, v):
        if v not in ['inline', 'attachment']:
            raise ValueError("Disposition must be 'inline' or 'attachment'")
        return v

class EmailSubject(BaseModel):
    subject: str

    @field_validator('subject')
    def validate_subject_length(cls, v):
        if v and len(v) > 998:
            raise ValueError("Subject must be less than 998 characters")
        return v

class EmailContent(BaseModel):
    html: Optional[str] = None
    text: Optional[str] = None
    template_id: Optional[str] = None
    
    @model_validator(mode='after')
    def validate_content_exists(cls, values):
        if values.html is None and values.text is None and values.template_id is None:
            raise ValueError("At least one of 'text', 'html' or 'template_id' must be provided")
        return values

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
    
    @field_validator('name')
    def validate_name(cls, v):
        if not v.replace('-', '').isalnum():
            raise ValueError("Header name must be alphanumeric and may contain '-'")
        return v

class EmailRequest(BaseModel):
    from_email: Optional[EmailFrom] = Field(None, alias="from")
    to: List[EmailRecipient]
    cc: Optional[List[EmailRecipient]] = None
    bcc: Optional[List[EmailRecipient]] = None
    reply_to: Optional[EmailReplyTo] = None
    subject: EmailSubject
    text: Optional[EmailContent] = None
    html: Optional[EmailContent] = None
    template_id: Optional[EmailContent] = None
    attachments: Optional[List[EmailAttachment]] = None
    tags: Optional[List[str]] = None
    personalization: Optional[List[EmailPersonalization]] = None
    precedence_bulk: Optional[bool] = None
    send_at: Optional[int] = None
    in_reply_to: Optional[str] = None
    references: Optional[List[str]] = None
    settings: Optional[EmailTrackingSettings] = None
    headers: Optional[List[EmailHeader]] = None

    model_config = ConfigDict(validate_by_name = True)
        
    @field_validator('tags')
    def validate_tags_count(cls, v):
        if v and len(v) > 5:
            raise ValueError("Maximum 5 tags are allowed")
        return v
        
    @field_validator('to')
    def validate_to_count(cls, v):
        if len(v) < 1 or len(v) > 50:
            raise ValueError("'to' must contain between 1 and 50 recipients")
        return v
        
    @field_validator('cc', 'bcc')
    def validate_cc_bcc_count(cls, v):
        if v and len(v) > 10:
            raise ValueError("Maximum 10 recipients allowed for cc/bcc")
        return v
        
