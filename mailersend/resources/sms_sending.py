from .base import BaseResource
from ..models.sms_sending import SmsSendRequest
from ..models.base import APIResponse
from ..exceptions import ValidationError


class SmsSending(BaseResource):
    """
    Client for interacting with the MailerSend SMS Sending API.
    """

    def send(self, request: SmsSendRequest) -> APIResponse:
        """
        Send an SMS message.
        
        Args:
            request: SmsSendRequest with SMS details
            
        Returns:
            APIResponse with SMS sending response and metadata
            
        Raises:
            ValidationError: If the request is invalid
            MailerSendError: If the API returns an error
        """
        self.logger.debug("Preparing to send SMS message")
        
        if not request:
            self.logger.error("No SmsSendRequest object provided")
            raise ValidationError("SmsSendRequest must be provided")
        
        if not isinstance(request, SmsSendRequest):
            self.logger.error("Invalid SmsSendRequest object provided")
            raise ValidationError("SmsSendRequest must be provided")
        
        # Convert to JSON payload
        payload = request.to_json()
        
        self.logger.info(f"Sending SMS to {len(request.to)} recipients")
        self.logger.debug(f"SMS payload: {payload}")
        
        response = self.client.request(method='POST', endpoint='sms', body=payload)
        
        return self._create_response(response)