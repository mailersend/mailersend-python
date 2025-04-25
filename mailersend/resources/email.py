from datetime import datetime
from typing import Dict, Any, List

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
        """
        self.logger.debug("Preparing to send emails in bulk")

        payload = []
        for email in emails:
            if not isinstance(email, EmailRequest):
                self.logger.error("Invalid EmailRequest object provided")
                raise ValidationError("EmailRequest must be provided")
            
            # Prepare payload for each email
            email_payload = email.model_dump(by_alias=True, exclude_none=True)
            payload.append(email_payload)

        self.logger.info("Sending email request to MailerSend API")
        self.logger.debug(f"Payload: {payload}")

        response = self.client.request("POST", "bulk-email", body=payload)

        return response.json()
    
    def get_bulk_status(self, bulk_email_id: str) -> Dict[str, Any]:
        """
        Get the status of a bulk email send request.

        Args:
            bulk_email_id: The ID of the bulk email request

        Returns:
            API response with bulk email status
        """
        self.logger.debug("Getting bulk email status")

        if not bulk_email_id:
            self.logger.error("No bulk email ID provided")
            raise ValidationError("Bulk email ID must be provided")

        response = self.client.request("GET", f"bulk-email/{bulk_email_id}")

        return response.json()