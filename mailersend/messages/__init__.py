"""
Handles /messages endpoint
Doc: https://developers.mailersend.com/api/v1/messages.html
"""

import requests
from mailersend.base import base


class NewMessage(base.NewAPIClient):
    """
    Instantiates the /messages endpoint object
    """

    pass

    def get_message_by_id(self, message_id):
        """
        Returns a JSON response from the MailerSend API
        """

        request = requests.get(
            f"{self.api_base}/messages/{message_id}", headers=self.headers_default
        )
        return request.text

    def get_messages(self):
        """
        Returns a JSON response from the MailerSend API
        """

        request = requests.get(
            f"{self.api_base}/messages", headers=self.headers_default
        )
        return request.text
