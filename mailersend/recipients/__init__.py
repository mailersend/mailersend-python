import requests
from mailersend.base import base


class NewRecipient(base.NewAPIClient):
    def __init__(self):
        baseobj = base.NewAPIClient()
        super(NewRecipient, self).__init__(
            baseobj.api_base,
            baseobj.headers_default,
            baseobj.headers_auth,
            baseobj.mailersend_api_key,
        )

    def get_recipients(self):

        request = requests.get(
            f"{self.api_base}/recipients", headers=self.headers_default
        )
        return request.text

    def get_recipient_by_id(self, recipient_id):

        request = requests.get(
            f"{self.api_base}/recipients/{recipient_id}", headers=self.headers_default
        )
        return request.text

    def delete_recipient(self, recipient_id):

        request = requests.delete(
            f"{self.api_base}/recipients/{recipient_id}", headers=self.headers_default
        )
        return request.status_code
