"""
Handles /recipients endpoint
Doc: https://developers.mailersend.com/api/v1/recipients.html
"""

import requests
from mailersend.base import base


class NewRecipient(base.NewAPIClient):
    """
    Instantiates the /recipients endpoint object
    """

    def __init__(self):
        """
        NewRecipient constructor
        """
        baseobj = base.NewAPIClient()
        super().__init__(
            baseobj.api_base,
            baseobj.headers_default,
            baseobj.headers_auth,
            baseobj.mailersend_api_key,
        )

    def get_recipients(self):
        """
        Returns a JSON response from the MailerSend API
        """

        request = requests.get(
            f"{self.api_base}/recipients", headers=self.headers_default
        )
        return request.text

    def get_recipient_by_id(self, recipient_id):
        """
        Returns a JSON response from the MailerSend API
        """

        request = requests.get(
            f"{self.api_base}/recipients/{recipient_id}", headers=self.headers_default
        )
        return request.text

    def delete_recipient(self, recipient_id):
        """
        Returns a HTTP status code from the MailerSend API
        """

        request = requests.delete(
            f"{self.api_base}/recipients/{recipient_id}", headers=self.headers_default
        )
        return request.status_code
