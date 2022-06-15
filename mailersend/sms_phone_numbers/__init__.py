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
            f"{self.api_base}/sms-numbers", headers=self.headers_default, params=query_params
        )

        return f"{request.status_code}\n{request.text}"



    def delete_phone_number(self):
        pass
