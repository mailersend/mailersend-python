import json
import os
import requests

API_BASE = "https://api.mailersend.com/v1"
API_KEY = os.environ.get("MAILERSEND_API_KEY")


class NewAPIClient(object):
    def __init__(
        self,
        api_base=None,
        headers_default=None,
        headers_auth=None,
        mailersend_api_key=None,
    ):

        self.api_base = API_BASE
        self.mailersend_api_key = API_KEY
        self.headers_auth = f"Bearer {self.mailersend_api_key}"
        self.headers_default = {
            "Content-Type": "application/json",
            "X-Requested-With": "XMLHttpRequest",
            "User-Agent": "MailerSend-Client-python-v1",
            "Authorization": f"{self.headers_auth}",
        }

    def generateConfigChangeBody(self, key, value):
        self.key = key
        self.value = value

        data = {key: value}

        return data
