import requests
from mailersend.base import base


class NewMessage(base.NewAPIClient):
    def __init__(self):
        baseobj = base.NewAPIClient()
        super(NewMessage, self).__init__(
            baseobj.api_base,
            baseobj.headers_default,
            baseobj.headers_auth,
            baseobj.mailersend_api_key,
        )

    def get_message_by_id(self, message_id):

        request = requests.get(
            f"{self.api_base}/messages/{message_id}", headers=self.headers_default
        )
        return request.text

    def get_messages(self):
        request = requests.get(
            f"{self.api_base}/messages", headers=self.headers_default
        )
        return request.text
