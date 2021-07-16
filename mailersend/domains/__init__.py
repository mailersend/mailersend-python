import requests
from mailersend.base import base


class NewDomain(base.NewAPIClient):
    def __init__(self):
        baseObj = base.NewAPIClient()
        super(NewDomain, self).__init__(
            baseObj.api_base,
            baseObj.headers_default,
            baseObj.headers_auth,
            baseObj.mailersend_api_key,
        )

    def getDomains(self):
        request = requests.get(f"{self.api_base}/domains", headers=self.headers_default)
        return request.text

    def getDomainById(self, domainId):
        self.domainId = domainId

        request = requests.get(
            f"{self.api_base}/domains/{domainId}", headers=self.headers_default
        )
        return request.text

    def deleteDomain(self, domainId):
        self.domainId = domainId

        request = requests.delete(
            f"{self.api_base}/domains/{domainId}", headers=self.headers_default
        )
        return request.status_code

    def getRecipientsForDomain(self, domainId):
        self.domainId = domainId

        request = requests.get(
            f"{self.api_base}/domains/{domainId}/recipients",
            headers=self.headers_default,
        )
        return request.text

    def updateDomainSetting(self, domainId, key, value):
        self.domainId = domainId

        data = {f"{key}": value}

        request = requests.put(
            f"{self.api_base}/domains/{domainId}/settings",
            headers=self.headers_default,
            json=data,
        )
        return request.text
