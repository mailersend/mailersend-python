"""
Handles /sms-webhooks endpoint
"""

import requests
from mailersend.base import base


class NewSmsWebhooks(base.NewAPIClient):
    """
    Instantiates the /sms-webhooks endpoint object
    """

    # you shall not
    pass

    def get_webhooks(self, sms_number_id):
        """
        Get a list of SMS webhooks.

        @params:
          sms_number_id (string)
        """

        passed_arguments = locals()
        query_params = {"sms_number_id": sms_number_id}

        request = requests.get(
            f"{self.api_base}/sms-webhooks",
            headers=self.headers_default,
            params=query_params,
        )

        return f"{request.status_code}\n{request.text}"

    def get_webhook(self, sms_webhook_id):
        """
        Get a single SMS webhook.

        @params:
          sms_webhook_id (string)
        """

        request = requests.get(
            f"{self.api_base}/sms-webhooks/{sms_webhook_id}",
            headers=self.headers_default,
        )

        return f"{request.status_code}\n{request.text}"

    def create_webhook(self, url, name, events, sms_number_id, enabled=True):
        """
        Create an SMS webhook.

        @params:
          url (string)
          name (string)
          events (dict)
          enabled (bool)
          sms_number_id (string)
        """

        data = {
            "url": url,
            "name": name,
            "events": events,
            "sms_number_id": sms_number_id,
            "enabled": int(enabled),
        }

        request = requests.post(
            f"{self.api_base}/sms-webhooks", headers=self.headers_default, json=data
        )

        return f"{request.status_code}\n{request.text}"

    def update_webhook(
        self, sms_webhook_id, url=None, name=None, events=None, enabled=None
    ):
        """
        Update a single SMS Webhook.

        @params:
          sms_webhook_id (string)
          url (string)
          name (string)
          events (dict)
          enabled (bool)
        """

        passed_arguments = locals()
        data = {}

        for key, value in passed_arguments.items():
            if key != "self" and key != "sms_webhook_id" and value is not None:
                if key == "enabled":
                    data[key] = int(value)
                else:
                    data[key] = value

        request = requests.put(
            f"{self.api_base}/sms-webhooks/{sms_webhook_id}",
            headers=self.headers_default,
            json=data,
        )

        return f"{request.status_code}\n{request.text}"

    def delete_webhook(self, sms_webhook_id):
        """
        Delete an SMS webhook.

        @params:
          sms_webhook_id (string)
        """

        request = requests.delete(
            f"{self.api_base}/sms-webhooks/{sms_webhook_id}",
            headers=self.headers_default,
        )

        return f"{request.status_code}\n{request.text}"
