import requests
from mailersend.base import base


class NewTemplate(base.NewAPIClient):
    def __init__(self):
        baseobj = base.NewAPIClient()
        super(NewTemplate, self).__init__(
            baseobj.api_base,
            baseobj.headers_default,
            baseobj.headers_auth,
            baseobj.mailersend_api_key,
        )

    def get_templates(self):
        request = requests.get(
            f"{self.api_base}/templates", headers=self.headers_default
        )
        return request.text

    def get_template_by_id(self, template_id):
        request = requests.get(
            f"{self.api_base}/templates/{template_id}", headers=self.headers_default
        )
        return request.text

    def delete_template(self, template_id):
        request = requests.delete(
            f"{self.api_base}/templates/{template_id}", headers=self.headers_default
        )
        return request.text
