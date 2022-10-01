"""
Handles /sms-recipients endpoint
"""

import requests
from mailersend.base import base


class NewSmsRecipients(base.NewAPIClient):
    """
    Instantiates the /sms-recipients endpoint object
    """

    pass

    def get_recipients(self, status="active", sms_number_id=None, page=None, limit=25):
        """
        Get information about SMS recipients.

        @params:
          status (string) - Possible values are `active` and `opt_out`
          sms_number_id (string)
          page (int)
          limit (int): Min: `10`, Max: `100`, default is 25
        """

        passed_arguments = locals()
        query_params = {}

        for key, value in passed_arguments.items():
            if key != "self":
                query_params[key] = value

        request = requests.get(
            f"{self.api_base}/sms-recipients",
            headers=self.headers_default,
            params=query_params,
        )

        return f"{request.status_code}\n{request.text}"

    def get_recipient(self, sms_recipient_id):
        """
        Get information about a specific SMS recipient.

        @params:
          sms_recipient_id (string) - Possible values are `active` and `opt_out`
        """

        request = requests.get(
            f"{self.api_base}/sms-recipients/{sms_recipient_id}",
            headers=self.headers_default,
        )

        return f"{request.status_code}\n{request.text}"

    def update_recipient(self, sms_recipient_id, status):
        """
        Update a specific SMS recipient

        @params:
          sms_recipient_id (string)
          status (string)
        """

        query_params = {"status": status}
        data = {"sms_recipient_id": sms_recipient_id}

        request = requests.put(
            f"{self.api_base}/sms-recipients/{sms_recipient_id}",
            headers=self.headers_default,
            params=query_params,
            json=data,
        )

        return f"{request.status_code}\n{request.text}"
