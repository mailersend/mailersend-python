"""
Handles /sms endpoint
"""

import requests
from mailersend.base import base


class NewSmsSending(base.NewAPIClient):
    """
    Instantiates the /sms endpoint object
    """

    pass

    def send_sms(self, number_from, numbers_to, text, personalization=None):
        """
        Send SMS message to one or more recipients

        Returns the JSON response of MailerSend API

        @params:
          number_from (str): Number belonging to your account in E164 format
          numbers_to (dict): Recipient phone numbers (up to 50)
          text (str): Message test
          personalization: Allows using personalization in {{ var }} syntax. Can be used in the text fields
        """

        data = {
            "from": number_from,
            "to": numbers_to,
            "text": text,
            "personalization": personalization,
        }

        if personalization is None:
            data["personalization"] = []

        request = requests.post(
            f"{self.api_base}/sms", headers=self.headers_default, json=data
        )

        return f"{request.status_code}\n{request.headers['X-SMS-Message-Id']}"
