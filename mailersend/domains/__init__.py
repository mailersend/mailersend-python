import requests
from mailersend.base import base


class NewDomain(base.NewAPIClient):
    def __init__(self):
        baseobj = base.NewAPIClient()
        super(NewDomain, self).__init__(
            baseobj.api_base,
            baseobj.headers_default,
            baseobj.headers_auth,
            baseobj.mailersend_api_key,
        )

    def get_domains(self):

        request = requests.get(f"{self.api_base}/domains", headers=self.headers_default)
        return request.text

    def get_domain_by_id(self, domain_id):

        request = requests.get(
            f"{self.api_base}/domains/{domain_id}", headers=self.headers_default
        )
        return request.text

    def delete_domain(self, domain_id):

        request = requests.delete(
            f"{self.api_base}/domains/{domain_id}", headers=self.headers_default
        )
        return request.status_code

    def get_recipients_for_domain(self, domain_id):

        request = requests.get(
            f"{self.api_base}/domains/{domain_id}/recipients",
            headers=self.headers_default,
        )
        return request.text

    def update_domain_setting(self, domain_id, key, value):

        data = {f"{key}": value}

        request = requests.put(
            f"{self.api_base}/domains/{domain_id}/settings",
            headers=self.headers_default,
            json=data,
        )
        return request.text
