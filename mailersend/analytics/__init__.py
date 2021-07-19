import requests
from mailersend.base import base


class NewAnalytics(base.NewAPIClient):
    def __init__(self):
        baseobj = base.NewAPIClient()
        super(NewAnalytics, self).__init__(
            baseobj.api_base,
            baseobj.headers_default,
            baseobj.headers_auth,
            baseobj.mailersend_api_key,
        )

    def get_activity_by_date(
        self, date_from, date_to, event, domainId=None, groupBy=None
    ):

        _data = {
            "date_from": date_from,
            "date_to": date_to,
            "event": event,
        }

        if domainId is not None:
            _data["domain_id"] = domainId

        if groupBy is not None:
            _data["group_by"] = groupBy

        request = requests.get(
            f"{self.api_base}/analytics/date", headers=self.headers_default, json=_data
        )

        return request.text

    def get_opens_by_country(self, date_from, date_to, domain_id=None, recipients=None):

        _data = {
            "date_from": self.dateFrom,
            "date_to": self.dateTo,
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
