from datetime import datetime
from typing import Dict, Any, List, Optional, Union

from .base import BaseResource
from ..models.email import EmailRequest
from ..exceptions import ValidationError
from ..utils.files import process_file_attachments
from ..utils.validators import validate_email_requirements


class Email(BaseResource):
    """
    Client for interacting with the MailerSend Email API.
    """
    
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
                - send_at (Union[int, datetime], optional): Scheduled send time
                - in_reply_to (str, optional): Valid email address as per RFC 2821
                - references (str, optional): List of Message-ID's that the current email is referencing
                - settings (Dict, optional): Tracking settings (opens, clicks, content)
                - headers (Dict, optional): Custom headers to include in the email
                
        Returns:
            API response with email ID
            
        Raises:
            ValidationError: If the email data is invalid
            MailerSendError: If the API returns an error
            
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

            >>> # With file attachments
            >>> client.email.send(
            ...     from_email={"email": "sender@example.com"},
            ...     to=[{"email": "recipient@example.com"}],
            ...     subject="Document Attached",
            ...     html="<p>See attached file</p>",
            ...     attachments=[{
            ...         "file_path": "/path/to/document.pdf",
            ...         "disposition": "attachment"
            ...     }]
            ... )
        """
        self.logger.debug("Preparing to send email")

        if not email and kwargs:
            # Convert from_email key for proper serialization
            if 'from_email' in kwargs:
                kwargs['from'] = kwargs.pop('from_email')
            
            # Process attachments if file_path is provided
            if 'attachments' in kwargs and isinstance(kwargs['attachments'], list):
                self._process_file_attachments(kwargs['attachments'])
                
            # Convert send_at from datetime to timestamp if needed
            if 'send_at' in kwargs and isinstance(kwargs['send_at'], datetime):
                kwargs['send_at'] = int(kwargs['send_at'].timestamp())
                
            try:
                email = EmailRequest(**kwargs)
                self.logger.debug("Created email request from kwargs")
            except Exception as e:
                self.logger.error(f"Failed to create email request: {str(e)}")
                raise ValidationError(f"Invalid email parameters: {str(e)}")
        
        if not email:
            self.logger.error("No email data provided")
            raise ValidationError("Either email object or email parameters must be provided")

        # Additional validation of dependencies
        try:
            validate_email_requirements(email)
        except ValidationError as e:
            self.logger.error(f"Email validation failed: {str(e)}")
            raise
        
        self.logger.info("Sending email request to API")

        response = self.client.request(
            "POST",
            "/email",
            body=email.dict(by_alias=True, exclude_none=True)
        )
        
        return response.json()
    
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