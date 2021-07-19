import requests
from mailersend.base import base


class NewActivity(base.NewAPIClient):
    def __init__(self):
        baseobj = base.NewAPIClient()
        super(NewActivity, self).__init__(
            baseobj.api_base,
            baseobj.headers_default,
            baseobj.headers_auth,
            baseobj.mailersend_api_key,
        )

    def getDomainActivity(
        self, domain_id, page=None, limit=None, date_from=None, date_to=None, event=None
    ):

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
