"""
Handles /analytics endpoint
Doc: https://developers.mailersend.com/api/v1/analytics.html
"""

import requests
from mailersend.base import base


class NewAnalytics(base.NewAPIClient):
    """
    Instantiates the /activity endpoint object
    """

    pass

    def get_activity_by_date(
        self, date_from, date_to, event, domain_id=None, group_by=None
    ):
        """
        Returns a JSON response from the MailerSend API
        """

        _data = {
            "date_from": date_from,
            "date_to": date_to,
            "event": event,
        }

        if domain_id is not None:
            _data["domain_id"] = domain_id

        if group_by is not None:
            _data["group_by"] = group_by

        request = requests.get(
            f"{self.api_base}/analytics/date", headers=self.headers_default, json=_data
        )

        return request.text

    def get_opens_by_country(self, date_from, date_to, domain_id=None, recipients=None):
        """
        Returns a JSON response from the MailerSend API
        """

        _data = {
            "date_from": date_from,
            "date_to": date_to,
        }

        if domain_id is not None:
            _data["domain_id"] = domain_id

        if recipients is not None:
            _data["recipient_id"] = recipients

        request = requests.get(
            f"{self.api_base}/analytics/country",
            headers=self.headers_default,
            json=_data,
        )

        return request.text

    def get_opens_by_user_agent(
        self, date_from, date_to, domain_id=None, recipients=None
    ):
        """
        Returns a JSON response from the MailerSend API
        """

        _data = {
            "date_from": date_from,
            "date_to": date_to,
        }

        if domain_id is not None:
            _data["domain_id"] = domain_id

        if recipients is not None:
            _data["recipient_id"] = recipients

        request = requests.get(
            f"{self.api_base}/analytics/ua-name",
            headers=self.headers_default,
            json=_data,
        )

        return request.text

    def get_opens_by_reading_environment(
        self, date_from, date_to, domain_id=None, recipients=None
    ):
        """
        Returns a JSON response from the MailerSend API
        """

        _data = {
            "date_from": date_from,
            "date_to": date_to,
        }

        if domain_id is not None:
            _data["domain_id"] = domain_id

        if recipients is not None:
            _data["recipient_id"] = recipients

        request = requests.get(
            f"{self.api_base}/analytics/ua-type",
            headers=self.headers_default,
            json=_data,
        )

        return request.text
