"""
Provides helper functions to convenience devs
"""

import requests
from mailersend.base import base


class NewHelper(base.NewAPIClient):
    """
    NewHelper extends base.NewAPIClient to inherit connection details
    """

    def __init__(self):
        """
        NewHelper constructor
        """
        pass

    def get_id_by_name(self, category, name):
        """
        Returns an ID given a category and item name from the MailerSend API

        @params:
          category (str): Can be one of "recipients", "domains"
          name (str): Object name
        """

        request = requests.get(
            f"{self.api_base}/{category}", headers=self.headers_default
        )

        _json_req = request.json()

        category_search_asset = {"recipients": "email", "domains": "name"}

        _data_block = _json_req["data"]

        for data in _data_block:
            if data[category_search_asset.get(category)] == name:
                return data["id"]

        return request.text
