"""
Handles /sms-activity endpoint
"""

import requests
from mailersend.base import base


class NewSmsActivity(base.NewAPIClient):
    """
    Instantiates the /sms-activity endpoint object
    """

    pass

    def get_activities(
        self,
        sms_number_id=None,
        date_from=None,
        date_to=None,
        status=[],
        page=None,
        limit=25,
    ):
        """
        Retrieve every single data point of the activity that happened for a specific phone number.

        @params:
          sms_number_id (str)
          date_from (int): Timestamp is assumed to be `UTC`. Must be lower than `date_to`
          date_to (int): Timestamp is assumed to be `UTC`. Must be higher than `date_from`
          status (dict): Possible types: `processed`,`queued`,`sent`,`delivered`, `failed`
          page (int)
          limit (int): Min: `10`, Max: `100`, default is 25
        """

        passed_arguments = locals()
        query_params = {}

        for key, value in passed_arguments.items():
            if key != "self":
                if key == "status":
                    query_params[key + "[]"] = value
                else:
                    query_params[key] = value

        request = requests.get(
            f"{self.api_base}/sms-activity",
            headers=self.headers_default,
            params=query_params,
        )

        return f"{request.status_code}\n{request.text}"

    def get_activity(self, sms_message_id):
        """
        Get every single activity data point that happened to a specific SMS message

        @params:
          sms_message_id (str)
        """

        request = requests.get(
            f"{self.api_base}/sms-messages/{sms_message_id}",
            headers=self.headers_default,
        )

        return f"{request.status_code}\n{request.text}"
