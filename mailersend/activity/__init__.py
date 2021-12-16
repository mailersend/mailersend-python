"""
Handles /activity endpoint
Doc: https://developers.mailersend.com/api/v1/activity.html
"""

import requests
from mailersend.base import base


class NewActivity(base.NewAPIClient):
    """
    Instantiates the /activity endpoint object
    """

    pass

    def get_domain_activity(
        self, domain_id, page=None, limit=None, date_from=None, date_to=None, event=None
    ):
        """
        Returns a JSON response from the MailerSend API
        """

        _data = {
            "page": page or None,
            "limit": limit or None,
            "dateFrom": date_from or None,
            "dateTo": date_to or None,
            "event": event or None,
        }

        request = requests.get(
            f"{self.api_base}/activity/{domain_id}",
            headers=self.headers_default,
            json=_data,
        )
        return request.text
