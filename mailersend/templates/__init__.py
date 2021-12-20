"""
Handles /templates endpoint
Doc: https://developers.mailersend.com/api/v1/templates.html
"""

import requests
from mailersend.base import base


class NewTemplate(base.NewAPIClient):
    """
    Instantiates the /templates endpoint object
    """

    pass

    def get_templates(self):
        """
        Returns a JSON response from the MailerSend API
        """
        request = requests.get(
            f"{self.api_base}/templates", headers=self.headers_default
        )
        return request.text

    def get_template_by_id(self, template_id):
        """
        Returns a JSON response from the MailerSend API
        """
        request = requests.get(
            f"{self.api_base}/templates/{template_id}", headers=self.headers_default
        )
        return request.text

    def delete_template(self, template_id):
        """
        Returns a JSON response from the MailerSend API
        """
        request = requests.delete(
            f"{self.api_base}/templates/{template_id}", headers=self.headers_default
        )
        return request.text
