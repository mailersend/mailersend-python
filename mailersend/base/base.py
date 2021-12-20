"""
Base object handles connection information to the MailerSend API
"""

import os

API_BASE = "https://api.mailersend.com/v1"
API_KEY = os.environ.get("MAILERSEND_API_KEY")


class NewAPIClient:
    """
    Instantiates the parent object all endpoints follow.
    Provides necessary connection information to perform API operations.
    """

    def __init__(
        self,
        mailersend_api_key=API_KEY,
        api_base=None,
        headers_default=None,
        headers_auth=None,
    ):
        """
        NewAPIClient constructor
        """

        self.api_base = API_BASE
        self.mailersend_api_key = mailersend_api_key
        self.headers_auth = f"Bearer {self.mailersend_api_key}"
        self.headers_default = {
            "Content-Type": "application/json",
            "X-Requested-With": "XMLHttpRequest",
            "User-Agent": "MailerSend-Client-python-v1",
            "Authorization": f"{self.headers_auth}",
        }


def generate_config_change_json_body(key, value):
    """
    Returns a key:value pair
    """
    data = {key: value}

    return data
