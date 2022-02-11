"""
Handles /message-schedules endpoint
Doc: https://developers.mailersend.com/api/v1/message-schedules.html
"""

import requests
from mailersend.base import base


class NewMessageSchedule(base.NewAPIClient):
    """
    Instantiates the /message-schedules endpoint object
    """

    pass

    def get_scheduled_messages(self):
        """
        Returns a JSON response from the MailerSend API
        """

        request = requests.get(
            f"{self.api_base}/message-schedules", headers=self.headers_default
        )
        return request.text

    def get_scheduled_message_by_id(self, message_id):
        """
        Returns a JSON response from the MailerSend API
        """

        request = requests.get(
            f"{self.api_base}/message-schedules/{message_id}",
            headers=self.headers_default,
        )
        return request.text

    def delete_scheduled_message(self, message_id):
        """
        Returns a JSON response from the MailerSend API
        """

        request = requests.delete(
            f"{self.api_base}/message-schedules/{message_id}",
            headers=self.headers_default,
        )
        return request.text
