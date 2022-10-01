"""
Handles /sms-numbers endpoint
"""

import requests
from mailersend.base import base


class NewSmsNumbers(base.NewAPIClient):
    """
    Instantiates the /sms-numbers endpoint object
    """

    pass

    def get_phone_numbers(self, paused=False, page=None, limit=25):
        """
        Get a list of SMS phone numbers information.

        @params:
          paused (bool)
          page (int)
          limit (int): Min: `10`, Max: `100`, default is 25
        """

        passed_arguments = locals()
        query_params = {}

        for key, value in passed_arguments.items():
            if key != "self":
                if key == "paused":
                    query_params[key] = int(value)
                else:
                    query_params[key] = value

        request = requests.get(
            f"{self.api_base}/sms-numbers",
            headers=self.headers_default,
            params=query_params,
        )

        return f"{request.status_code}\n{request.text}"

    def get_phone_number(self, sms_number_id):
        """
        Get information about a specific SMS phone number

        @params:
          sms_number_id (string)
        """

        request = requests.get(
            f"{self.api_base}/sms-numbers/{sms_number_id}", headers=self.headers_default
        )

        return f"{request.status_code}\n{request.text}"

    def update_phone_number(self, sms_number_id, paused=True):
        """
        Update a specific SMS phone number

        @params:
          sms_number_id (string)
           paused (bool)
        """

        query_params = {"paused": int(paused)}
        data = {"sms_number_id": sms_number_id}

        request = requests.put(
            f"{self.api_base}/sms-numbers/{sms_number_id}",
            headers=self.headers_default,
            params=query_params,
            json=data,
        )

        return f"{request.status_code}\n{request.text}"

    def delete_phone_number(self, sms_number_id):
        """
        Delete a specific SMS phone number

        @params:
          sms_number_id (string)
        """

        data = {"sms_number_id": sms_number_id}

        request = requests.delete(
            f"{self.api_base}/sms-numbers/{sms_number_id}",
            headers=self.headers_default,
            json=data,
        )

        return f"{request.status_code}\n{request.text}"
