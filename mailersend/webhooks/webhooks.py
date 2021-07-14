import requests
from mailersend.base import base

data = {}


class NewWebhook(base.NewAPIClient):
    def __init__(self):
        baseObj = base.NewAPIClient()
        super(NewWebhook, self).__init__(
            baseObj.api_base,
            baseObj.headers_default,
            baseObj.headers_auth,
            baseObj.mailersend_api_key,
        )

    def getWebhooks(self, domain_id):
        request = requests.get(
            f"{self.api_base}/webhooks",
            headers=self.headers_default,
            json={"domain_id": domain_id},
        )
        return request.text

    def getWebhookByID(self, webhook_id):
        request = requests.get(
            f"{self.api_base}/webhooks/{webhook_id}", headers=self.headers_default
        )
        return request.text

    def setWebhookURL(self, webhook_url):
        data["url"] = webhook_url

    def setWebhookName(self, webhook_name):
        data["name"] = webhook_name

    def setWebhookEvents(self, events):
        data["events"] = events

    def setWebhookEnabled(self, enabled=True):
        data["enabled"] = enabled

    def setWebhookDomain(self, domain_id):
        data["domain_id"] = domain_id

    def updateWebhook(self, webhook_id, key, value):
        request = requests.put(
            f"{self.api_base}/webhooks/{webhook_id}",
            headers=self.headers_default,
            json={f"{key}": value},
        )
        return request.text

    def deleteWebhook(self, webhook_id):
        request = requests.delete(
            f"{self.api_base}/webhooks/{webhook_id}", headers=self.headers_default
        )
        return request.text

    def createWebhook(self):
        request = requests.post(
            f"{self.api_base}/webhooks", headers=self.headers_default, json=data
        )
        return request.text
