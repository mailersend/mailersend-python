import requests
from mailersend.base import base


class NewMessage(base.NewAPIClient):
    def __init__(self):
        baseObj = base.NewAPIClient()
        super(NewMessage, self).__init__(
            baseObj.api_base,
            baseObj.headers_default,
            baseObj.headers_auth,
            baseObj.mailersend_api_key,
        )

    def getMessageById(self, messageId):
        self.messageId = messageId

        request = requests.get(
            f"{self.api_base}/messages/{messageId}", headers=self.headers_default
        )
        return request.text

    def getMessages(self):
        request = requests.get(
            f"{self.api_base}/messages", headers=self.headers_default
        )
        return request.text
