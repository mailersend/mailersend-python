import requests
from mailersend.base import base


class NewToken(base.NewAPIClient):
    def __init__(self):
        baseObj = base.NewAPIClient()
        super(NewToken, self).__init__(
            baseObj.api_base,
            baseObj.headers_default,
            baseObj.headers_auth,
            baseObj.mailersend_api_key,
        )

    def createToken(self, tokenName, tokenScopes):
        self.tokenName = tokenName
        self.tokenScopes = tokenScopes

        _data = {"name": tokenName, "scopes": tokenScopes}

        request = requests.post(
            f"{self.api_base}/token", headers=self.headers_default, json=_data
        )
        return request.text

    def updateToken(self, tokenId, pause=True):
        self.tokenId = tokenId
        self.pause = pause

        if pause == True:
            _data = self.generateConfigChangeBody("status", "pause")
        else:
            _data = self.generateConfigChangeBody("status", "unpause")

        request = requests.put(
            f"{self.api_base}/token/{tokenId}/settings",
            headers=self.headers_default,
            json=_data,
        )
        return request.text

    def deleteToken(self, tokenId):
        self.tokenId = tokenId

        request = requests.delete(
            f"{self.api_base}/token/{tokenId}/", headers=self.headers_default
        )
        return request.status_code
