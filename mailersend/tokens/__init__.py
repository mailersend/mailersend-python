import requests
from mailersend.base import base


class NewToken(base.NewAPIClient):
    def __init__(self):
        baseobj = base.NewAPIClient()
        super(NewToken, self).__init__(
            baseobj.api_base,
            baseobj.headers_default,
            baseobj.headers_auth,
            baseobj.mailersend_api_key,
        )

    def create_token(self, token_name, token_scopes):

        _data = {"name": token_name, "scopes": token_scopes}

        request = requests.post(
            f"{self.api_base}/token", headers=self.headers_default, json=_data
        )
        return request.text

    def update_token(self, token_id, pause=True):

        if pause:
            _data = self.generate_config_change_json_body("status", "pause")
        else:
            _data = self.generate_config_change_json_body("status", "unpause")

        request = requests.put(
            f"{self.api_base}/token/{token_id}/settings",
            headers=self.headers_default,
            json=_data,
        )
        return request.text

    def delete_token(self, token_id):

        request = requests.delete(
            f"{self.api_base}/token/{token_id}/", headers=self.headers_default
        )
        return request.status_code
