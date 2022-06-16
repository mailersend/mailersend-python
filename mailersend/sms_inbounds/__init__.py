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
        pass

    def get_inbound_route(self, sms_inbound_id):
        pass

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
