"""Messages resource"""

from .base import BaseResource
from ..models.messages import (
    MessagesListRequest,
    MessageGetRequest,
)
from ..models.base import APIResponse


class Messages(BaseResource):
    """
    Client for interacting with the MailerSend Messages API.

    Provides methods for retrieving message information.
    """

    def list_messages(self, request: MessagesListRequest) -> APIResponse:
        """
        Retrieve a list of messages.

        Args:
            request: MessagesListRequest with pagination options

        Returns:
            APIResponse containing the messages list response
        """
        self.logger.debug("Preparing to list messages with query parameters")

        # Extract query parameters
        params = request.to_query_params()

        self.logger.debug("Making API request to list messages with params: %s", params)

        # Make API request
        response = self.client.request(
            method="GET", endpoint="messages", params=params if params else None
        )

        return self._create_response(response)

    def get_message(self, request: MessageGetRequest) -> APIResponse:
        """
        Retrieve information about a single message.

        Args:
            request: MessageGetRequest with message ID

        Returns:
            APIResponse containing the message response
        """
        self.logger.debug("Preparing to get message with ID: %s", request.message_id)

        # Make API request
        response = self.client.request(
            method="GET", endpoint=f"messages/{request.message_id}"
        )

        return self._create_response(response)
