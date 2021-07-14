import requests
from mailersend.base import base


class NewRecipient(base.NewAPIClient):
    def __init__(self):
        baseObj = base.NewAPIClient()
        super(NewRecipient, self).__init__(
            baseObj.api_base,
            baseObj.headers_default,
            baseObj.headers_auth,
            baseObj.mailersend_api_key,
        )

    def getRecipients(self):
        request = requests.get(
            f"{self.api_base}/recipients", headers=self.headers_default
        )
        return request.text

    def getRecipientByID(self, recipientId):
        self.recipientId = recipientId
        request = requests.get(
            f"{self.api_base}/recipients/{recipientId}", headers=self.headers_default
        )
        return request.text

    def deleteRecipient(self, recipientId):
        self.recipientId = recipientId
        request = requests.delete(
            f"{self.api_base}/recipients/{recipientId}", headers=self.headers_default
        )
        return request.status_code
