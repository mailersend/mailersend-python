"""
Handles /sms-messages endpoint
"""

import requests
from mailersend.base import base


class NewSmsMessages(base.NewAPIClient):
    """
    Instantiates the /sms-messages endpoint object
    """

    pass

    def get_messages(self, page=1, limit=25):
        """
        Get a list of SMS messages.

        @params:
          page (int)
          limit (int): Min: `10`, Max: `100`, default is 25
        """

        passed_arguments = locals()
        query_params = {}

        for key, value in passed_arguments.items():
            query_params[key] = value

        request = requests.get(
            f"{self.api_base}/sms-messages",
            headers=self.headers_default,
            params=query_params,
        )

        return f"{request.status_code}\n{request.text}"

    def get_message(self, sms_message_id):
        """
        Get a single SMS message.

        @params:
          sms_message_id (string)
        """

        request = requests.get(
            f"{self.api_base}/sms-messages/{sms_message_id}",
            headers=self.headers_default,
        )

        return f"{request.status_code}\n{request.text}"
