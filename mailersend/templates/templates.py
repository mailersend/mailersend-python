import requests
from mailersend.base import base


class NewTemplate(base.NewAPIClient):
    def __init__(self):
        baseObj = base.NewAPIClient()
        super(NewTemplate, self).__init__(
            baseObj.api_base,
            baseObj.headers_default,
            baseObj.headers_auth,
            baseObj.mailersend_api_key,
        )

    def getTemplates(self):
        request = requests.get(
            f"{self.api_base}/templates", headers=self.headers_default
        )
        return request.text

    def getTemplateByID(self, template_id):
        request = requests.get(
            f"{self.api_base}/templates/{template_id}", headers=self.headers_default
        )
        return request.text

    def deleteTemplate(self, template_id):
        request = requests.delete(
            f"{self.api_base}/templates/{template_id}", headers=self.headers_default
        )
        return request.text
