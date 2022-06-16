"""
Handles /sms-inbounds endpoint
"""

import requests
from mailersend.base import base


class NewSmsInbounds(base.NewAPIClient):
    """
    Instantiates the /sms-inbounds endpoint object
    """

    # you shall not
    pass

    def get_inbound_routes(self, sms_number_id=None, enabled=None, page=1, limit=25):
        """
        Get a list of SMS inbound routes.

        @params:
          sms_number_id (string)
          enabled (bool)
          page (int)
          limit (int)
        """

        passed_arguments = locals()
        query_params = {}

        for key, value in passed_arguments.items():
            if key != "self":
                if key == "enabled":
                    query_params[key] = int(value)
                else:
                    query_params[key] = value

        request = requests.get(
            f"{self.api_base}/sms-inbounds", headers=self.headers_default, params=query_params
        )

        return f"{request.status_code}\n{request.text}"

    def get_inbound_route(self, sms_inbound_id):
        """
        Get a single SMS inbound route.

        @params:
          sms_inbound_id (string)
        """

        request = requests.get(
            f"{self.api_base}/sms-inbounds/{sms_inbound_id}", headers=self.headers_default
        )

        return f"{request.status_code}\n{request.text}"

    def create_inbound_route(self, sms_number_id, name, forward_url, filter, enabled=True):
        pass

    def update_inbound_route(self, sms_inbound_id, sms_number_id, name, forward_url, filter, enabled=True):
        pass

    def delete_inbound_route(self, sms_inbound_id):
        """
        Delete an SMS inbound route.

        @params:
          sms_inbound_id (string)
        """

        request = requests.delete(
            f"{self.api_base}/sms-inbounds/{sms_inbound_id}", headers=self.headers_default
        )

        return f"{request.status_code}\n{request.text}"
