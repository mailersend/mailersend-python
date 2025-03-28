import base64
from typing import Dict, Any, List, Optional, Union, BinaryIO
from datetime import datetime
import mimetypes

from .base import BaseResource
from ..models.email import (
    EmailRequest, EmailStatus, EmailRecipient, EmailFrom, 
    EmailPersonalization, EmailAttachment, EmailTemplate,
    EmailTracking, BulkEmailRequest, EmailActivity
)


class Email(BaseResource):
    """
    Client for interacting with the MailerSend Email API.
    """
    
    BASE_API_URL = "api/v1"
    
    def send(self, 
             email: Optional[EmailRequest] = None,
             **kwargs: Any) -> Dict[str, Any]:
        """
        Send a single email.
        
        You can either pass a complete EmailRequest object or build the email using
        keyword arguments.
        
        Args:
            email: A complete EmailRequest object
            **kwargs: Email components as keyword args:
                - from_email (Dict): Sender information with 'email' and 'name'
                - to (List): List of recipients with 'email' and 'name'
                - subject (str): Email subject
                - text (str, optional): Plain text version of the email
                - html (str, optional): HTML version of the email
                - template_id (str, optional): ID of the template to use
                - personalization (List, optional): Personalization variables
                - cc (List, optional): CC recipients
                - bcc (List, optional): BCC recipients
                - reply_to (Dict, optional): Reply-to address
                - attachments (List, optional): List of attachments
                - tags (List, optional): Tags for categorizing
                - tracking (Dict, optional): Tracking settings
                - precedence_bulk (bool, optional): Bulk precedence
                - send_at (integer, optional): Scheduled send time (Unix timestamp)
                - in_reply_to (str, optional): Valid email address as per RFC 2821
                - references (str, optional): List of Message-ID's that the current email is referencing
                - settings (Dict, optional): Can only contain the keys: track_clicks, track_opens and track_content and a boolean value of true or false.
                - headers (Dict, optional): Custom headers to include in the email
                
        Returns:
            API response with email ID
            
        Raises:
            ValidationError: If the email data is invalid
            
        Examples:
            >>> # Using keyword arguments
            >>> client.email.send(
            ...     from_email={"email": "sender@example.com", "name": "Sender"},
            ...     to=[{"email": "recipient@example.com", "name": "Recipient"}],
            ...     subject="Hello",
            ...     html="<p>Hello, world!</p>"
            ... )
            
            >>> # Using EmailRequest object
            >>> request = EmailRequest(
            ...     from_email=EmailFrom(email="sender@example.com", name="Sender"),
            ...     to=[EmailRecipient(email="recipient@example.com", name="Recipient")],
            ...     subject="Hello",
            ...     html="<p>Hello, world!</p>"
            ... )
            >>> client.email.send(email=request)
        """
        if not email and kwargs:
            # Convert from_email key for proper serialization
            if 'from_email' in kwargs:
                kwargs['from'] = kwargs.pop('from_email')
            
            email = EmailRequest(**kwargs)
        
        if not email:
            raise ValueError("Either email object or email parameters must be provided")
            
        return self.client.request(
            "POST",
            f"{self.BASE_API_URL}/email",
            body=email.dict(by_alias=True)
        ).json()
    
    def send_bulk(self, emails: List[EmailRequest]) -> Dict[str, Any]:
        """
        Send multiple emails in one request.
        
        Args:
            emails: List of EmailRequest objects to send
            
        Returns:
            API response with bulk email information
            
        Examples:
            >>> requests = [
            ...     EmailRequest(
            ...         from_email=EmailFrom(email="sender@example.com", name="Sender"),
            ...         to=[EmailRecipient(email="recipient1@example.com", name="Recipient 1")],
            ...         subject="Hello 1",
            ...         html="<p>Hello, recipient 1!</p>"
            ...     ),
            ...     EmailRequest(
            ...         from_email=EmailFrom(email="sender@example.com", name="Sender"),
            ...         to=[EmailRecipient(email="recipient2@example.com", name="Recipient 2")],
            ...         subject="Hello 2",
            ...         html="<p>Hello, recipient 2!</p>"
            ...     )
            ... ]
            >>> client.email.send_bulk(requests)
        """
        bulk_data = {"messages": [email.dict(by_alias=True) for email in emails]}
        
        return self.client.request(
            "POST",
            f"{self.BASE_API_URL}/bulk-email",
            body=bulk_data
        ).json()
    
    def get_status(self, email_id: str) -> EmailStatus:
        """
        Get the status of an email.
        
        Args:
            email_id: ID of the email to check
            
        Returns:
            EmailStatus object with current status
            
        Examples:
            >>> status = client.email.get_status("email_123456")
            >>> print(f"Email status: {status.status}")
        """
        response = self.client.request(
            "GET",
            f"{self.BASE_API_URL}/email/{email_id}/status"
        )
        
        return EmailStatus(**response.json())
    
    def get_settings(self) -> Dict[str, Any]:
        """
        Get default email settings.
        
        Returns:
            Current email settings
            
        Examples:
            >>> settings = client.email.get_settings()
        """
        return self.client.request(
            "GET",
            f"{self.BASE_API_URL}/email/settings"
        ).json()
    
    def update_settings(self, settings: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update default email settings.
        
        Args:
            settings: New settings to apply
            
        Returns:
            Updated settings
            
        Examples:
            >>> updated = client.email.update_settings({
            ...     "track_opens": True,
            ...     "track_clicks": True
            ... })
        """
        return self.client.request(
            "PUT",
            f"{self.BASE_API_URL}/email/settings",
            body=settings
        ).json()
    
    def get_domain_settings(self, domain_id: str) -> Dict[str, Any]:
        """
        Get domain tracking settings.
        
        Args:
            domain_id: ID of the domain
            
        Returns:
            Current domain settings
            
        Examples:
            >>> domain_settings = client.email.get_domain_settings("domain_123456")
        """
        return self.client.request(
            "GET",
            f"{self.BASE_API_URL}/domains/{domain_id}/settings"
        ).json()
    
    def update_domain_settings(self, domain_id: str, settings: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update domain tracking settings.
        
        Args:
            domain_id: ID of the domain
            settings: New settings to apply
            
        Returns:
            Updated domain settings
            
        Examples:
            >>> updated = client.email.update_domain_settings("domain_123456", {
            ...     "track_opens": True,
            ...     "track_clicks": True
            ... })
        """
        return self.client.request(
            "PUT",
            f"{self.BASE_API_URL}/domains/{domain_id}/settings",
            body=settings
        ).json()
    
    def get_activity(self, 
                     activity_type: str,
                     domain_id: Optional[str] = None,
                     limit: Optional[int] = None,
                     page: Optional[int] = None) -> Dict[str, Any]:
        """
        Get email activity of a specific type.
        
        Args:
            activity_type: Type of activity to retrieve (opened, clicked, etc.)
            domain_id: Optional domain ID to filter by
            limit: Number of records per page
            page: Page number
            
        Returns:
            Email activity data
            
        Examples:
            >>> opened = client.email.get_activity("opened", limit=100)
            >>> clicked = client.email.get_activity("clicked", domain_id="domain_123456")
        """
        params = {}
        if domain_id:
            params["domain_id"] = domain_id
        if limit:
            params["limit"] = limit
        if page:
            params["page"] = page
            
        return self.client.request(
            "GET",
            f"{self.BASE_API_URL}/email/activity/{activity_type}",
            params=params
        ).json()
    
    def add_attachment(self, 
                       filename: str, 
                       content: Union[str, bytes, BinaryIO]) -> EmailAttachment:
        """
        Helper method to create an email attachment object.
        
        Args:
            filename: Name of the file
            content: File content as string, bytes or file-like object
            
        Returns:
            EmailAttachment object ready to use with send() method
            
        Examples:
            >>> with open("document.pdf", "rb") as f:
            ...     attachment = client.email.add_attachment("document.pdf", f)
            >>> email_request.attachments = [attachment]
        """
        # Determine how to handle the content
        if hasattr(content, 'read'):
            # File-like object
            content_bytes = content.read()
            if isinstance(content_bytes, str):
                content_bytes = content_bytes.encode('utf-8')
        elif isinstance(content, str):
            # String content
            content_bytes = content.encode('utf-8') 
        else:
            # Assuming bytes
            content_bytes = content
            
        # Encode to base64
        content_base64 = base64.b64encode(content_bytes).decode('utf-8')
        
        # Determine content type
        content_type = mimetypes.guess_type(filename)[0] or 'application/octet-stream'
        
        # Create attachment object
        return EmailAttachment(
            content=content_base64,
            filename=filename,
            disposition="attachment",
            id=None
        )