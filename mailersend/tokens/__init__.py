"""
Handles /tokens endpoint
Doc: https://developers.mailersend.com/api/v1/tokens.html
"""

import requests
from mailersend.base import base


class NewToken(base.NewAPIClient):
    """
    Instantiates the /tokens endpoint object
    """

    pass

    def create_token(self, token_name, token_scopes):
        """
        Returns a JSON response from the MailerSend API
        """

        _data = {"name": token_name, "scopes": token_scopes}

        request = requests.post(
            f"{self.api_base}/token", headers=self.headers_default, json=_data
        )
        return request.text

    def update_token(self, token_id, pause=True):
        """
        Returns a JSON response from the MailerSend API
        """

        if pause:
            _data = base.generate_config_change_json_body("status", "pause")
        else:
            _data = base.generate_config_change_json_body("status", "unpause")

        request = requests.put(
            f"{self.api_base}/token/{token_id}/settings",
            headers=self.headers_default,
            json=_data,
        )
        return request.text

    def delete_token(self, token_id):
        """
        Returns a HTTP status code from the MailerSend API
        """

        request = requests.delete(
            f"{self.api_base}/token/{token_id}/", headers=self.headers_default
        )
        return request.status_code
