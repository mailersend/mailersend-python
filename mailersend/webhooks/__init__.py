import requests
from mailersend.base import base

data = {}


class NewWebhook(base.NewAPIClient):
    def __init__(self):
        baseobj = base.NewAPIClient()
        super(NewWebhook, self).__init__(
            baseobj.api_base,
            baseobj.headers_default,
            baseobj.headers_auth,
            baseobj.mailersend_api_key,
        )

    def get_webhooks(self, domain_id):
        request = requests.get(
            f"{self.api_base}/webhooks",
            headers=self.headers_default,
            json={"domain_id": domain_id},
        )
        return request.text

    def get_webhook_by_id(self, webhook_id):
        request = requests.get(
            f"{self.api_base}/webhooks/{webhook_id}", headers=self.headers_default
        )
        return request.text

    def set_webhook_url(self, webhook_url):
        data["url"] = webhook_url

    def set_webhook_name(self, webhook_name):
        data["name"] = webhook_name

    def set_webhook_events(self, events):
        data["events"] = events

    def set_webhook_enabled(self, enabled=True):
        data["enabled"] = enabled

    def set_webhook_domain(self, domain_id):
        data["domain_id"] = domain_id

    def update_webhook(self, webhook_id, key, value):
        request = requests.put(
            f"{self.api_base}/webhooks/{webhook_id}",
            headers=self.headers_default,
            json={f"{key}": value},
        )
        return request.text

    def delete_webhook(self, webhook_id):
        request = requests.delete(
            f"{self.api_base}/webhooks/{webhook_id}", headers=self.headers_default
        )
        return request.text

    def create_webhook(self):
        request = requests.post(
            f"{self.api_base}/webhooks", headers=self.headers_default, json=data
        )
        return request.text
