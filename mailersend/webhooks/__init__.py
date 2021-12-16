"""
Handles /webhooks endpoint
Doc: https://developers.mailersend.com/api/v1/webhooks.html
"""

import requests
from mailersend.base import base

data = {}


class NewWebhook(base.NewAPIClient):
    """
    Instantiates the /webhooks endpoint object
    """

    def __init__(self):
        """
        NewWebhook constructor
        """
        pass

    def get_webhooks(self, domain_id):
        """
        Returns a JSON response from the MailerSend API

        @params:
          domain_id (str): A domain ID
        """
        request = requests.get(
            f"{self.api_base}/webhooks",
            headers=self.headers_default,
            json={"domain_id": domain_id},
        )
        return request.text

    def get_webhook_by_id(self, webhook_id):
        """
        Returns a JSON response from the MailerSend API

        @params:
          webhook_id (str): A webhook ID
        """
        request = requests.get(
            f"{self.api_base}/webhooks/{webhook_id}", headers=self.headers_default
        )
        return request.text

    def set_webhook_url(self, webhook_url):
        """
        Sets the webhook 'url' field

        @params:
          webhook_url (str): A webhook URL
        """
        data["url"] = webhook_url

    def set_webhook_name(self, webhook_name):
        """
        Sets the webhook 'name' field

        @params:
          webhook_name (str): A webhook name
        """

        data["name"] = webhook_name

    def set_webhook_events(self, events):
        """
        Sets the webhook 'events' field

        @params:
          events (list): A list containing valid events
        """
        data["events"] = events

    def set_webhook_enabled(self, enabled=True):
        """
        Sets the webhook 'enabled' status field

        @params:
          enabled (bool): Controls webhook status
        """

        data["enabled"] = enabled

    def set_webhook_domain(self, domain_id):
        """
        Sets the webhook 'domain_id' status field

        @params:
          domain_id (str): A valid domain ID
        """

        data["domain_id"] = domain_id

    def update_webhook(self, webhook_id, key, value):
        """
        Updates a webhook setting

        @params:
          webhook_id (str): A valid webhook ID
          key (str): A setting key
          value (str): Corresponding keys value
        """

        request = requests.put(
            f"{self.api_base}/webhooks/{webhook_id}",
            headers=self.headers_default,
            json={f"{key}": value},
        )
        return request.text

    def delete_webhook(self, webhook_id):
        """
        Returns a JSON response from the MailerSend API

        @params:
          webhook_id (str): A valid webhook ID
        """

        request = requests.delete(
            f"{self.api_base}/webhooks/{webhook_id}", headers=self.headers_default
        )
        return request.text

    def create_webhook(self):
        """
        Returns a JSON response from the MailerSend API
        """

        request = requests.post(
            f"{self.api_base}/webhooks", headers=self.headers_default, json=data
        )
        return request.text
