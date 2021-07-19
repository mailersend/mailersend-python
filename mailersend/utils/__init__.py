import requests
from mailersend.base import base


class NewHelper(base.NewAPIClient):
    def __init__(self):
        baseobj = base.NewAPIClient()
        super(NewHelper, self).__init__(
            baseobj.api_base,
            baseobj.headers_default,
            baseobj.headers_auth,
            baseobj.mailersend_api_key,
        )

    def get_id_by_name(self, category, name):

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
