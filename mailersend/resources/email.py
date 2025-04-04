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

    def send(self, email: EmailRequest = None) -> Dict[str, Any]:
        """
        Send a single email.

        Args:
            email: A fully-validated EmailRequest object

        Returns:
            API response with email ID

        Raises:
            ValidationError: If the EmailRequest is invalid
            MailerSendError: If the API returns an error
        """
        self.logger.debug("Preparing to send email")

        if not email:
            self.logger.error("No EmailRequest object provided")
            raise ValidationError("EmailRequest must be provided")

        payload = email.model_dump(by_alias=True, exclude_none=True)

        self.logger.info("Sending email request to MailerSend API")
        self.logger.debug(f"Payload: {payload}")

        response = self.client.request("POST", "email", body=payload)
        
        return {
            "id": response.headers.get("x-message-id")
        }
    

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