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
                
        Returns:
            API response with email ID
            
        Raises:
            ValidationError: If the email data is invalid
            MailerSendError: If the API returns an error
            
        Examples:
            >>> # Using EmailRequest object
            >>> request = EmailRequest(
            ...     from_email=EmailFrom(email="sender@example.com", name="Sender"),
            ...     to=[EmailRecipient(email="recipient@example.com", name="Recipient")],
            ...     subject=EmailSubject(subject="Hello"),
            ...     html=EmailContent(html="<p>Hello, world!</p>")
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
                process_file_attachments(kwargs['attachments'])
                
            # Convert send_at from datetime to timestamp if needed
            if 'send_at' in kwargs and isinstance(kwargs['send_at'], datetime):
                kwargs['send_at'] = int(kwargs['send_at'].timestamp())
                
            try:
                email = self._create_email_request(kwargs)
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
        print(email.model_dump(by_alias=True, exclude_none=True))

        # response = self.client.request(
        #     "POST",
        #     "email",
        #     body=email.model_dump(by_alias=True, exclude_none=True)
        # )
        
        # return response.json()
    
    def _create_email_request(self, kwargs: Dict[str, Any]) -> EmailRequest:
        """
        Create an EmailRequest from keyword arguments.
        
        Args:
            kwargs: The keyword arguments to convert
            
        Returns:
            An EmailRequest instance
        """
        from mailersend.models.email import EmailRequest, EmailFrom, EmailRecipient, EmailSubject, EmailContent, EmailReplyTo
        
        # Clone the kwargs to avoid modifying the original
        processed = kwargs.copy()
        
        # Convert from_email to from field if needed
        if 'from_email' in processed and 'from' not in processed:
            processed['from'] = processed.pop('from_email')
        
        # Handle 'from' field - create EmailFrom object if it's a dict
        if 'from' in processed and isinstance(processed['from'], dict):
            processed['from'] = EmailFrom(**processed['from'])
        
        # Handle recipient fields - create EmailRecipient objects if they're dicts
        for field in ['to', 'cc', 'bcc']:
            if field in processed and isinstance(processed[field], list):
                processed[field] = [
                    EmailRecipient(**r) if isinstance(r, dict) else r
                    for r in processed[field]
                ]
        
        # Handle 'reply_to' field - create EmailReplyTo object if it's a dict
        if 'reply_to' in processed and isinstance(processed['reply_to'], dict):
            processed['reply_to'] = EmailReplyTo(**processed['reply_to'])
        
        # Create proper model objects for these fields (not nested)
        if 'subject' in processed and isinstance(processed['subject'], str):
            # Create EmailSubject instance directly
            processed['subject'] = EmailSubject(subject=processed['subject'])
        
        if 'html' in processed and not isinstance(processed['html'], EmailContent):
            if isinstance(processed['html'], str):
                processed['html'] = EmailContent(html=processed['html'])
            elif isinstance(processed['html'], dict):
                processed['html'] = EmailContent(**processed['html'])
        
        if 'text' in processed and not isinstance(processed['text'], EmailContent):
            if isinstance(processed['text'], str):
                processed['text'] = EmailContent(text=processed['text'])
            elif isinstance(processed['text'], dict):
                processed['text'] = EmailContent(**processed['text'])
        
        if 'template_id' in processed and not isinstance(processed['template_id'], EmailContent):
            if isinstance(processed['template_id'], str):
                processed['template_id'] = EmailContent(template_id=processed['template_id'])
            elif isinstance(processed['template_id'], dict):
                processed['template_id'] = EmailContent(**processed['template_id'])
        
        # Create and return the EmailRequest
        self.logger.debug(f"Creating EmailRequest with: {processed}")
        return EmailRequest(**processed)

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