import requests
from mailersend.base import base


class NewHelper(base.NewAPIClient):
    def __init__(self):
        baseObj = base.NewAPIClient()
        super(NewHelper, self).__init__(
            baseObj.api_base,
            baseObj.headers_default,
            baseObj.headers_auth,
            baseObj.mailersend_api_key,
        )

    def getIDByName(self, category, name):
        self.category = category
        self.name = name

        request = requests.get(
            f"{self.api_base}/{category}", headers=self.headers_default
        )

        _json_req = request.json()

        category_search_asset = {"recipients": "email", "domains": "name"}

        _data_block = _json_req["data"]

        for data in _data_block:
            if data[category_search_asset.get(category)] == name:
                return data["id"]
            else:
                raise ValueError("Not found")

        return request.text
