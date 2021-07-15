import requests
from mailersend.base import base


class NewAnalytics(base.NewAPIClient):
    def __init__(self):
        baseObj = base.NewAPIClient()
        super(NewAnalytics, self).__init__(
            baseObj.api_base,
            baseObj.headers_default,
            baseObj.headers_auth,
            baseObj.mailersend_api_key,
        )

    def getActivityByDate(self, dateFrom, dateTo, event, domainId=None, groupBy=None):
        self.domainId = domainId
        self.dateFrom = dateFrom
        self.dateTo = dateTo
        self.groupBy = groupBy
        self.event = event

        _data = {
            "date_from": dateFrom,
            "date_to": dateTo,
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

    def getOpensByCountry(self, dateFrom, dateTo, domainId=None, recipients=None):
        self.domainId = domainId
        self.dateFrom = dateFrom
        self.dateTo = dateTo
        self.recipients = recipients

        _data = {
            "date_from": self.dateFrom,
            "date_to": self.dateTo,
        }

        if domainId is not None:
            _data["domain_id"] = domainId

        if recipients is not None:
            _data["recipient_id"] = groupBy

        request = requests.get(
            f"{self.api_base}/analytics/country",
            headers=self.headers_default,
            json=_data,
        )

        return request.text

    def getOpensByUserAgent(self, dateFrom, dateTo, domainId=None, recipients=None):
        self.domainId = domainId
        self.dateFrom = dateFrom
        self.dateTo = dateTo
        self.recipients = recipients

        _data = {
            "date_from": self.dateFrom,
            "date_to": self.dateTo,
        }

        if domainId is not None:
            _data["domain_id"] = domainId

        if recipients is not None:
            _data["recipient_id"] = groupBy

        request = requests.get(
            f"{self.api_base}/analytics/ua-name",
            headers=self.headers_default,
            json=_data,
        )

        return request.text

    def getOpensByReadingEnvironment(
        self, dateFrom, dateTo, domainId=None, recipients=None
    ):
        self.domainId = domainId
        self.dateFrom = dateFrom
        self.dateTo = dateTo
        self.recipients = recipients

        _data = {
            "date_from": self.dateFrom,
            "date_to": self.dateTo,
        }

        if domainId is not None:
            _data["domain_id"] = domainId

        if recipients is not None:
            _data["recipient_id"] = groupBy

        request = requests.get(
            f"{self.api_base}/analytics/ua-type",
            headers=self.headers_default,
            json=_data,
        )

        return request.text
